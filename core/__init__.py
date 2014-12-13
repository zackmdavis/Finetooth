from django.apps import AppConfig

from core.signals import log_failed_login

class FinetoothConfig(AppConfig):
    name = "core"
    verbose_name = "Finetooth Core"

    def ready(self):
        import core.signals

default_app_config = "core.FinetoothConfig"
