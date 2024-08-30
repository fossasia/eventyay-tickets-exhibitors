from django.urls import path, re_path

from .views import SettingsView, ExhibitorListView, ExhibitorCreateView

urlpatterns = [
    path('control/event/<str:organizer>/<str:event>/settings/exhibitors/',
        SettingsView.as_view(), name='settings'),
    re_path(r'^control/event/(?P<organizer>[^/]+)/(?P<event>[^/]+)/exhibitors/',
        ExhibitorListView.as_view(), name='info'),
    re_path(r'^control/event/(?P<organizer>[^/]+)/(?P<event>[^/]+)/exhibitors/add$',
        ExhibitorCreateView.as_view(), name='add'),

]
