# apps.py
from django.apps import AppConfig

class MainAppConfig(AppConfig):
    """
    Configuración principal para la aplicación 'main_app'.
    
    Esta configuración incluye la inicialización automática de señales al arrancar la aplicación.
    """
    name = 'main_app'  # Nombre de la aplicación, utilizado por Django para registrar la aplicación

    def ready(self):
        """
        Método que se ejecuta cuando la aplicación está lista.
        
        Aquí importamos las señales de la aplicación para asegurarnos de que estén registradas y activas.
        Esto es útil para acciones automáticas, como la creación de perfiles de usuario al registrarse.
        """
        import main_app.signals  # Importamos señales para que estén listas cuando la aplicación se inicializa
        



