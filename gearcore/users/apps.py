import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "gearcore.users"
    verbose_name = _("Користувачі")

    def ready(self):
        with contextlib.suppress(ImportError):
            import gearcore.users.signals  # noqa: F401
