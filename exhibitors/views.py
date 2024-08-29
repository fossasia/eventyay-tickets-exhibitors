from django import forms
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.utils.translation import gettext, gettext_lazy as _
from pretix.base.forms import SettingsForm
from pretix.base.models import Event
from pretix.control.permissions import EventPermissionRequiredMixin
from django.views.generic import ListView
from pretix.control.views.event import (
    EventSettingsFormView, EventSettingsViewMixin,
)
from .models import ExhibitorInfo


class ExhibitorSettingForm(SettingsForm):
    exhibitor_url = forms.URLField(
        label=_("Exhibitor URL"),
        required=False,
    )

    exhibitor_name = forms.CharField(
        label=_("Exhibitor Name"),
        required=True,
    )

    exhibitor_description = forms.CharField(
        label=_("Exhibitor Description"),
        required=False,
    )

    exhibitor_logo = forms.ImageField(
        label=_("Exhibitor Logo"),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        self.obj = kwargs.get('obj')
        super().__init__(*args, **kwargs)

    def clean(self):
        data = super().clean()
        return data

class SettingsView(EventSettingsViewMixin, EventSettingsFormView):
    model = Event
    form_class = ExhibitorSettingForm
    template_name = 'exhibitors/settings.html'
    permission = 'can_change_settings'

    def get_success_url(self) -> str:
        return reverse('plugins:exhibitors:settings', kwargs={
            'organizer': self.request.event.organizer.slug,
            'event': self.request.event.slug
        })



class ExhibitorListView(EventPermissionRequiredMixin, ListView):
    model = ExhibitorInfo
    permission = ('can_change_event_settings', 'can_view_orders')
    template_name = 'exhibitors/exhibitor_info.html'
    context_object_name = 'layouts'

    def get_success_url(self) -> str:
        return reverse('plugins:exhibitors:index', kwargs={
            'organizer': self.request.event.organizer.slug,
            'event': self.request.event.slug
        })
