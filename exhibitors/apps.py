from django.utils.translation import gettext_lazy

from . import __version__

try:
    from pretix.base.plugins import PluginConfig
except ImportError:
    raise RuntimeError("Please use pretix 2.7 or above to run this plugin!")


class PluginApp(PluginConfig):
    default = True
    name = "exhibitors"
    verbose_name = "exhibitors"

    class PretixPluginMeta:
        name = gettext_lazy("exhibitors")
        author = "Srivatsav Auswin"
        description = gettext_lazy("This plugin enables to add and control exhibitors in eventyay")
        visible = True
        version = __version__
        category = "FEATURE"
        compatibility = "pretix>=2.7.0"

    def ready(self):
        from . import signals  # NOQA
