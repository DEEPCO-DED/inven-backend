from django.apps import AppConfig


class InvenappConfig(AppConfig):
    name = 'invenapp'
# apps.py
from django.apps import AppConfig

class YourAppNameConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'your_app_name'

    def ready(self):
        import invenapp.signals