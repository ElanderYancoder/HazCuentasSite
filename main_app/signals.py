# main_app/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile, ProgresoUsuario

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """Crea un perfil automáticamente cuando un nuevo usuario es registrado."""
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    """Guarda el perfil cada vez que el usuario es actualizado."""
    instance.profile.save()
    
    

# Secion para asignar las insigneas de manera automatica 

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import  Insignia, InsigniaUsuario

@receiver(post_save, sender=ProgresoUsuario)
def otorgar_insignia_post_curso(sender, instance, created, **kwargs):
    if created:  # Solo al registrar un nuevo curso completado
        usuario = instance.usuario
        curso = instance.leccion
        insignia = Insignia.objects.filter(nombre=f"Completó {curso.titulo}").first()
        if insignia and not InsigniaUsuario.objects.filter(usuario=usuario, insignia=insignia).exists():
            InsigniaUsuario.objects.create(
                usuario=usuario,
                insignia=insignia,
                motivo=f"Por completar el curso {curso.titulo}"
            )






'''
La señal se utiliza para generar una notificación
automáticamente cuando se registra la finalización de una lección.'''
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import LessonCompletion, Notificacion

@receiver(post_save, sender=LessonCompletion)
def send_lesson_completion_notification(sender, instance, created, **kwargs):
    if created:
        # Crear una notificación
        Notificacion.objects.create(
            usuario=instance.user,
            titulo="¡Lección completada!",
            mensaje=f"Has completado la lección '{instance.lesson}'. ¡Buen trabajo!"
        )



# Notificar a los suscriptores 

# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import BlogPost, Suscriptor

@receiver(post_save, sender=BlogPost)
def notificar_suscriptores(sender, instance, created, **kwargs):
    if created:
        suscriptores = Suscriptor.objects.values_list('email', flat=True)
        asunto = f"Nueva publicación: {instance.titulo}"
        mensaje = f"¡Hola! Hay una nueva publicación en el blog: {instance.titulo}\n\n{instance.contenido[:100]}...\n\nVisítala aquí: /blog/{instance.slug}/"
        send_mail(asunto, mensaje, 'tu_correo@ejemplo.com', suscriptores)



