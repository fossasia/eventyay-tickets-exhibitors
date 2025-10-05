from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

from . import __version__


class ExhibitorApp(AppConfig):
    name = "exhibitors"
    verbose_name = _("Exhibitors")

    class EventyayPluginMeta:
        name = _("Exhibitors")
        author = "FOSSASIA"
        description = _("This plugin enables to add and control exhibitors in eventyay")
        visible = True
        featured = True
        version = __version__
        category = "FEATURE"

    def ready(self):
        from . import signals  # NOQA


default_app_config = 'exhibitors.ExhibitorApp'
