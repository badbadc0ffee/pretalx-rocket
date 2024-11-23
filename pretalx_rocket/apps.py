from django.apps import AppConfig
from django.utils.translation import gettext_lazy

from . import __version__


class PluginApp(AppConfig):
    name = "pretalx_rocket"
    verbose_name = "pretalx Rocket.Chat plugin"

    class PretalxPluginMeta:
        name = gettext_lazy("pretalx Rocket.Chat plugin")
        author = "Florian Moesch"
        description = gettext_lazy(
            "pretalx plugin to send notifications about changes to submissions to a Rocket.Chat channel"
        )
        visible = True
        version = __version__
        category = "INTEGRATION"

    def ready(self):
        from . import signals  # NOQA
