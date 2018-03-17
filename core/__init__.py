from django.apps import AppConfig


class FinetoothConfig(AppConfig):
    name = "core"
    verbose_name = "Finetooth Core"

    def ready(self) -> None:
        import core.signals

default_app_config = "core.FinetoothConfig"
