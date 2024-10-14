from rest_framework import viewsets, views, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone

from pretix.base.models import OrderPosition
from pretix.api.serializers.i18n import I18nAwareModelSerializer
from pretix.api.serializers.order import CompatibleJSONField

from .models import ExhibitorInfo, ExhibitorItem, Lead


class ExhibitorAuthView(views.APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        key = request.data.get('key')

        if not email or not key:
            return Response(
                {'detail': 'Missing parameters'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            exhibitor = ExhibitorInfo.objects.get(email=email, key=key)
            return Response(
                {'success': True, 'exhibitor_id': exhibitor.id},
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

        # Check if the lead has already been scanned for this exhibitor
        if Lead.objects.filter(exhibitor=exhibitor, pseudonymization_id=pseudonymization_id).exists():
            return Response(
                {
                    'success': False,
                    'error': 'Lead already scanned'
                },
                status=status.HTTP_409_CONFLICT
            )
        # Try to retrieve the attendee's details using the pseudonymization_id
        try:
            order_position = OrderPosition.objects.get(
                pseudonymization_id=pseudonymization_id
            )
            attendee_name = order_position.attendee_name
            attendee_email = order_position.attendee_email
        except OrderPosition.DoesNotExist:
            return Response(
                {
                    'success': False,
                    'error': 'Attendee not found'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # Create the lead entry in the database
        lead = Lead.objects.create(
            exhibitor=exhibitor,
            pseudonymization_id=pseudonymization_id,
            scanned=timezone.now(),
            scan_type=scan_type,
            device_name=device_name,
            attendee={
                'name': attendee_name,
                'email': attendee_email
            }
        )

        return Response(
            {
                'success': True,
                'lead_id': lead.id
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
            'scanned',
            'scan_type',
            'device_name',
            'attendee'
        )

        return Response(
            {
                'success': True,
                'leads': list(leads)
            },
            status=status.HTTP_200_OK
        )
