from django.apps import AppConfig

class HealthProbeConfig(AppConfig):
    name = 'health_probe'

    def ready(self):
        from health_probe.scripts.health_checker import start_health_check
        start_health_check()

