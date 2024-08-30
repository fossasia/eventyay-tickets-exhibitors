from django import forms
from pretix.base.forms import SettingsForm
from django.utils.translation import gettext, gettext_lazy as _
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

class ExhibitorInfoForm(forms.ModelForm):
    class Meta:
        model = ExhibitorInfo
        fields = ['name', 'description', 'logo', 'url']
