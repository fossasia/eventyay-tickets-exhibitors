from django.urls import re_path as urls

from pretix.api.urls import event_router
from .api import ExhibitorInfoViewSet, ExhibitorItemViewSet

from .views import SettingsView, ExhibitorListView, ExhibitorCreateView, ExhibitorEditView, ExhibitorDeleteView, ExhibitorCopyKeyView

urlpatterns = [
    urls(r'^control/event/(?P<organizer>[^/]+)/(?P<event>[^/]+)/settings/exhibitors',
        SettingsView.as_view(), name='settings'),
    urls(r'^control/event/(?P<organizer>[^/]+)/(?P<event>[^/]+)/exhibitors$',
        ExhibitorListView.as_view(), name='info'),
    urls(r'^control/event/(?P<organizer>[^/]+)/(?P<event>[^/]+)/exhibitors/add$',
        ExhibitorCreateView.as_view(), name='add'),
    urls(r'^control/event/(?P<organizer>[^/]+)/(?P<event>[^/]+)/exhibitors/edit/(?P<pk>[^/]+)$',
         ExhibitorEditView.as_view(), name='edit'),
    urls(r'^control/event/(?P<organizer>[^/]+)/(?P<event>[^/]+)/exhibitors/delete/(?P<pk>[^/]+)$',
         ExhibitorDeleteView.as_view(), name='delete'),
    urls(r'^control/event/(?P<organizer>[^/]+)/(?P<event>[^/]+)/exhibitors/copy_key/(?P<pk>[^/]+)$',
         ExhibitorCopyKeyView.as_view(), name='copy_key'),
]

event_router.register('exhibitors', ExhibitorInfoViewSet, basename='exhibitorinfo')
event_router.register('exhibitoritems', ExhibitorItemViewSet, basename='exhibitoritem')
