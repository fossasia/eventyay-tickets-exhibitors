from django.db import transaction
from django.utils.functional import cached_property
from pretix.helpers.models import modelcopy
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.utils.translation import gettext, gettext_lazy as _
from pretix.base.forms import SettingsForm
from pretix.base.models import Event
from pretix.control.permissions import EventPermissionRequiredMixin
from django.views.generic import ListView, CreateView
from pretix.control.views.event import (
    EventSettingsFormView, EventSettingsViewMixin,
)
from .models import ExhibitorInfo
from .forms import ExhibitorSettingForm, ExhibitorInfoForm

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

class ExhibitorCreateView(EventPermissionRequiredMixin, CreateView):
    model = ExhibitorInfo
    form_class = ExhibitorInfoForm
    template_name = 'exhibitors/add.html'
    permission = 'can_change_event_settings'
    context_object_name = 'exhibitor'
    success_url = '/ignored'

    @transaction.atomic
    def form_valid(self, form):
        return redirect(reverse('plugins:exhibitor:add', kwargs={
            'organizer': self.request.event.organizer.slug,
            'event': self.request.event.slug,
            'layout': form.instance.pk
        }))

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        if self.copy_from:
            i = modelcopy(self.copy_from)
            i.pk = None
            i.default = False
            kwargs['instance'] = i
            kwargs.setdefault('initial', {})
        return kwargs

