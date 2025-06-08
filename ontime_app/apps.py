from django.apps import AppConfig

# --- Configuración Principal de la Aplicación ---

class OntimeAppConfig(AppConfig):
    """
    Clase de configuración para la aplicación 'ontime_app'.
    Se definen ajustes específicos para la aplicación.
    """
    # Define el tipo de campo automático predeterminado para las claves primarias de los modelos
    default_auto_field = 'django.db.models.BigAutoField'
    # Define el nombre de la aplicación
    name = 'ontime_app'

    def ready(self):
        """
        Método que se ejecuta cuando la aplicación está lista y completamente cargada por Django.
        Lugar ideal para importar módulos que contienen señales.
        """
        # Importa el módulo 'signals' de la aplicación 'ontime_app'.
        # Asegura que las señales definidas en 'signals.py' se conecten
        # correctamente a los modelos cuando la aplicación se inicia.
        import ontime_app.signals
