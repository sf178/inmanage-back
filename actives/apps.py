from django.apps import AppConfig


class ActivesAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'actives'

    def ready(self):
        import actives.signals