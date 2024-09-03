from rest_framework import viewsets

from pretix.api.serializers.i18n import I18nAwareModelSerializer
from pretix.api.serializers.order import CompatibleJSONField

from .models import ExhibitorInfo, ExhibitorItem


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
