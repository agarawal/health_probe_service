from django.apps import AppConfig
from django.db.utils import OperationalError

class HealthProbeConfig(AppConfig):
    name = 'health_probe'

    def ready(self):
        try:
            from health_probe.scripts.health_checker import start_health_check
            start_health_check()
        except OperationalError as e:
            # Handling the situation when there is no db table exists, especially when running the migrations and migrate command
            print(f"OperationalError occurred while initializing health probe: {e}")

