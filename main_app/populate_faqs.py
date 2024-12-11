from main_app.models import FAQ, Categoria

def run():
    # Crear categorías
    cat1, created = Categoria.objects.get_or_create(nombre="Cuenta y Seguridad", descripcion="Preguntas sobre cuentas y seguridad")
    cat2, created = Categoria.objects.get_or_create(nombre="Facturación y Pagos", descripcion="Preguntas sobre pagos y facturación")
    
    # Crear FAQs
    FAQ.objects.get_or_create(pregunta="¿Cómo recupero mi contraseña?", respuesta="Haz clic en 'Olvidé mi contraseña' y sigue las instrucciones.", categoria=cat1)
    FAQ.objects.get_or_create(pregunta="¿Cómo cambio mi plan de suscripción?", respuesta="Visita la sección 'Planes' en tu perfil.", categoria=cat2)
