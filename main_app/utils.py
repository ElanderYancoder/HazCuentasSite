from .models import Insignia, InsigniaUsuario, Notificacion

def otorgar_insignia_por_curso(usuario, curso):
    # Busca la insignia específica
    insignia = Insignia.objects.filter(nombre=f"Completó {curso.titulo}").first()
    if insignia:
        # Verifica si el usuario ya tiene esta insignia
        if not InsigniaUsuario.objects.filter(usuario=usuario, insignia=insignia).exists():
            InsigniaUsuario.objects.create(
                usuario=usuario,
                insignia=insignia,
                motivo=f"Por completar el curso {curso.titulo}"
            )



# ----------------------------------------------------------------
# funcion para enviar notificaciones 
def enviar_notificacion(titulo, mensaje, tipo_destinatario, usuario=None, grupo=None):
    if tipo_destinatario == 'usuario' and usuario:
        Notificacion.objects.create(
            tipo_destinatario='usuario',
            usuario=usuario,
            titulo=titulo,
            mensaje=mensaje
        )
    elif tipo_destinatario == 'grupo' and grupo:
        usuarios = grupo.user_set.all()
        for user in usuarios:
            Notificacion.objects.create(
                tipo_destinatario='grupo',
                usuario=user,
                grupo=grupo,
                titulo=titulo,
                mensaje=mensaje
            )
    elif tipo_destinatario == 'todos':
        usuarios = usuarios.objects.all()
        for user in usuarios:
            Notificacion.objects.create(
                tipo_destinatario='todos',
                usuario=user,
                titulo=titulo,
                mensaje=mensaje
            )
    else:
        raise ValueError("Debe proporcionar un usuario o grupo válido.")
    
    
    
    
    


# enviar notificaciones en tiempo real 
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

def enviar_notificacion_en_tiempo_real(user, title, message):
    channel_layer = get_channel_layer()
    group_name = f"user_{user.id}"

    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'send_notification',
            'title': title,
            'message': message
        }
    )

