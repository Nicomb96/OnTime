from django.apps import AppConfig

# Configuración principal de la app
class OntimeAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ontime_app'

    # Importa las señales al iniciar la app
    def ready(self):
        import ontime_app.signals
