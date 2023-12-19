from django.apps import AppConfig


class StatsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stats'

    def ready(self):
        print("Signals connected")
