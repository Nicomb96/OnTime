from django.apps import AppConfig


class OntimeAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ontime_app'
    def ready(self):
        import ontime_app.signals
