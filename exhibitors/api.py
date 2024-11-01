from django.shortcuts import get_object_or_404
from django.utils import timezone
from pretix.api.serializers.i18n import I18nAwareModelSerializer
from pretix.api.serializers.order import CompatibleJSONField
from pretix.base.models import OrderPosition
from rest_framework import status, views, viewsets
from rest_framework.response import Response

from .models import ExhibitorInfo, ExhibitorItem, ExhibitorTag, Lead


class ExhibitorAuthView(views.APIView):
    def post(self, request, *args, **kwargs):
        key = request.data.get('key')

        if not key:
            return Response(
                {'detail': 'Missing parameters'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            exhibitor = ExhibitorInfo.objects.get(key=key)
            return Response(
                {
                    'success': True,
                    'exhibitor_id': exhibitor.id,
                    'exhibitor_name': exhibitor.name,
                    'booth_id': exhibitor.booth_id,
                    'booth_name': exhibitor.booth_name,
                },
                status=status.HTTP_200_OK
            )
        except ExhibitorInfo.DoesNotExist:
            return Response(
                {'success': False, 'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )


class ExhibitorItemAssignmentSerializer(I18nAwareModelSerializer):
    class Meta:
        model = ExhibitorItem
        fields = ('id', 'item', 'exhibitor')


class NestedItemAssignmentSerializer(I18nAwareModelSerializer):
    class Meta:
        model = ExhibitorItem
        fields = ('item',)


class ExhibitorInfoSerializer(I18nAwareModelSerializer):
    class Meta:
        model = ExhibitorInfo
        fields = ('id', 'name', 'description', 'url', 'email', 'logo', 'key', 'lead_scanning_enabled')


class ExhibitorInfoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ExhibitorInfoSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return ExhibitorInfo.objects.filter(event=self.request.event)


class ExhibitorItemViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ExhibitorItemAssignmentSerializer
    queryset = ExhibitorItem.objects.none()
    lookup_field = 'id'

    def get_queryset(self):
        return ExhibitorItem.objects.filter(item__event=self.request.event)


class LeadCreateView(views.APIView):
    def post(self, request, *args, **kwargs):
        # Extract parameters from the request
        pseudonymization_id = request.data.get('lead')
        scanned = request.data.get('scanned')
        scan_type = request.data.get('scan_type')
        device_name = request.data.get('device_name')
        key = request.headers.get('Exhibitor')

        if not pseudonymization_id or not scanned or not scan_type or not device_name:
            return Response(
                {
                    'detail': 'Missing parameters'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Authenticate the exhibitor using the key
        try:
            exhibitor = ExhibitorInfo.objects.get(key=key)
        except ExhibitorInfo.DoesNotExist:
            return Response(
                {
                    'success': False,
                    'error': 'Invalid exhibitor key'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Try to retrieve the attendee's details using the pseudonymization_id
        try:
            order_position = OrderPosition.objects.get(
                pseudonymization_id=pseudonymization_id
            )
            attendee_name = order_position.attendee_name
            attendee_email = order_position.attendee_email
            country = order_position.country
            company = order_position.company
            city = order_position.city
            exhibitor = ExhibitorInfo.objects.get(key=key)
            exhibitor_name = exhibitor.name
            booth_id = exhibitor.booth_id
            booth_name = exhibitor.booth_name
        except OrderPosition.DoesNotExist:
            return Response(
                {
                    'success': False,
                    'error': 'Attendee not found'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # Check if the lead has already been scanned for this exhibitor
        if Lead.objects.filter(exhibitor=exhibitor, pseudonymization_id=pseudonymization_id).exists():
            return Response(
                {
                    'success': False,
                    'error': 'Lead already scanned',
                    'attendee': {
                        'name': attendee_name,
                        'email': attendee_email
                    }
                },
                status=status.HTTP_409_CONFLICT
            )

        # Create the lead entry in the database
        lead = Lead.objects.create(
            exhibitor=exhibitor,
            exhibitor_name=exhibitor_name,
            pseudonymization_id=pseudonymization_id,
            scanned=timezone.now(),
            scan_type=scan_type,
            device_name=device_name,
            booth_id=booth_id,
            booth_name=booth_name,
            attendee={
                'name': attendee_name,
                'email': attendee_email,
                'note': '',
                'tags': []
            }
        )

        return Response(
            {
                'success': True,
                'lead_id': lead.id,
                'attendee': {
                    'name': attendee_name,
                    'email': attendee_email
                }
            },
            status=status.HTTP_201_CREATED
        )


class LeadRetrieveView(views.APIView):
    def get(self, request, *args, **kwargs):
        # Authenticate the exhibitor using the key
        key = request.headers.get('Exhibitor')
        try:
            exhibitor = ExhibitorInfo.objects.get(key=key)
        except ExhibitorInfo.DoesNotExist:
            return Response(
                {
                    'success': False,
                    'error': 'Invalid exhibitor key'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Fetch all leads associated with the exhibitor
        leads = Lead.objects.filter(exhibitor=exhibitor).values(
            'id',
            'pseudonymization_id',
            'exhibitor_name',
            'scanned',
            'scan_type',
            'device_name',
            'booth_id',
            'booth_name',
            'attendee'
        )

        return Response(
            {
                'success': True,
                'leads': list(leads)
            },
            status=status.HTTP_200_OK
        )


class TagListView(views.APIView):
    def get(self, request, organizer, event, *args, **kwargs):
        key = request.headers.get('Exhibitor')
        try:
            exhibitor = ExhibitorInfo.objects.get(key=key)
            tags = ExhibitorTag.objects.filter(exhibitor=exhibitor)
            return Response({
                'success': True,
                'tags': [tag.name for tag in tags]
            })
        except ExhibitorInfo.DoesNotExist:
            return Response(
                {
                    'success': False,
                    'error': 'Invalid exhibitor key'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

class LeadUpdateView(views.APIView):
    def post(self, request, organizer, event, lead_id, *args, **kwargs):
        key = request.headers.get('Exhibitor')
        note = request.data.get('note')
        tags = request.data.get('tags', [])

        try:
            exhibitor = ExhibitorInfo.objects.get(key=key)
        except ExhibitorInfo.DoesNotExist:
            return Response(
                {
                    'success': False,
                    'error': 'Invalid exhibitor key'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            lead = Lead.objects.get(pseudonymization_id=lead_id, exhibitor=exhibitor)
        except Lead.DoesNotExist:
            return Response(
                {
                    'success': False,
                    'error': 'Lead not found'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # Update lead's attendee info
        attendee_data = lead.attendee or {}
        if note is not None:
            attendee_data['note'] = note
        if tags is not None:
            attendee_data['tags'] = tags

            # Update tag usage counts and create new tags
            for tag_name in tags:
                tag, created = ExhibitorTag.objects.get_or_create(
                    exhibitor=exhibitor,
                    name=tag_name
                )
                if not created:
                    tag.use_count += 1
                    tag.save()

        lead.attendee = attendee_data
        lead.save()
        
        return Response(
            {
                'success': True,
                'lead_id': lead.id,
                'attendee': lead.attendee
            },
            status=status.HTTP_200_OK
        )
