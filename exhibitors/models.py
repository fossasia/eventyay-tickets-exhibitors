import string
import json

from django.db import models
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _

from pretix.base.models import LoggedModel

class ExhibitorInfo(LoggedModel):
    name = models.CharField(
        max_length=190,
        verbose_name=_('Name')
    )
    description = models.TextField( 
        verbose_name=_('Description'),
        null=True,
        blank=True
    )
    url = models.URLField(
        verbose_name=_('URL'),
        null=True,
        blank=True
    )
    logo = models.FileField(
        verbose_name=_('Logo'),
        null=True,
        blank=True
    )


    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name
