from django.db import models
import string
import json
import random
import os
from django.utils.translation import gettext_lazy as _
from pretix.base.models import Event

def generate_key():
    return ''.join(random.choices(
        string.ascii_lowercase + string.digits, k=8
    ))

def exhibitor_logo_path(instance, filename):
    return os.path.join('exhibitors', 'logos', instance.name, filename)


class ExhibitorInfo(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
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
    email = models.EmailField(
        verbose_name=_('Email'),
        null=True,
        blank=True
    )
    logo = models.ImageField(
        upload_to=exhibitor_logo_path,
        null=True,
        blank=True
    )
    key = models.CharField(
        max_length=8,
        default=generate_key,
    )
    lead_scanning_enabled = models.BooleanField(
        default=True
    )

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name

class ExhibitorItem(models.Model):
    # If no ExhibitorItem exists => use default
    # If ExhibitorItem exists with layout=None => don't print
    item = models.OneToOneField('pretixbase.Item', null=True, blank=True, related_name='exhibitor_assignment',
                                on_delete=models.CASCADE)
    exhibitor = models.ForeignKey('ExhibitorInfo', on_delete=models.CASCADE, related_name='item_assignments',
                               null=True, blank=True)

    class Meta:
        ordering = ('id',)