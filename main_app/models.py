from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Modelo para Noticias
class Noticia(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    autor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    imagen = models.ImageField(upload_to='imagenes_noticias/', null=True, blank=True)
    destacado = models.BooleanField(default=False)  # Para marcar noticias importantes

    def __str__(self):
        return self.titulo




# Modelo para Módulo de Entrenamiento (la categoría principal del entrenamiento)
class ModuloEntrenamiento(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    video = models.FileField(upload_to='videos_entrenamiento/', blank=True, null=True)  # Para guardar el archivo de video
    fecha_creacion = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.titulo


# Modelo para Lección (lecciones individuales dentro de los módulos de entrenamiento)
# models.py
from django.db import models

class Leccion(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    contenido = models.TextField()
    imagen = models.ImageField(upload_to='lecciones/', null=True, blank=True)
    video = models.FileField(upload_to='videos/', null=True, blank=True)  # Campo para subir el video

    def __str__(self):
        return self.titulo


# Modelo para Progreso de Usuario
class ProgresoUsuario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    leccion = models.ForeignKey(Leccion, on_delete=models.CASCADE)
    completado = models.BooleanField(default=False)
    fecha_completado = models.DateTimeField(null=True, blank=True)  # Asegúrate de que sea DateTimeField

    def __str__(self):
        return f"{self.usuario.username} - {self.leccion.titulo} - {'Completado' if self.completado else 'Pendiente'}"

    


# Modelo para la retroalimentacion de usuario 
class Retroalimentacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    leccion = models.ForeignKey(Leccion, on_delete=models.CASCADE, related_name="retroalimentaciones")
    comentario = models.TextField()
    calificacion = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])  # Calificación de 1 a 5
    fecha = models.DateTimeField(auto_now_add=True)
    moderada = models.BooleanField(default=False)  # Nuevo campo para administración


    def __str__(self):
        return f"Retroalimentación de {self.usuario} para {self.leccion}"
    
    
# --------------------------------
# Area de testimonios de los clientes
class Plan_test(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    
    def __str__(self):
        return self.nombre


# models.py
#from django.db import models
from django.contrib.auth.models import User

class Testimonio(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    nombre = models.CharField(max_length=255)
    puesto = models.CharField(max_length=255, blank=True)
    comentario = models.TextField(max_length=500)
    foto = models.ImageField(upload_to='testimonios/', null=True, blank=True)
    enlace_redes = models.URLField(max_length=200, null=True, blank=True)
    estado = models.CharField(max_length=10, choices=[('pendiente', 'Pendiente'), ('aprobado', 'Aprobado')], default='pendiente')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Testimonio de {self.nombre} ({self.puesto})"



# ----------------------------------------------------------------
# area de centro de ayuda 

from django.db import models

# Definir las categorías
from django.db import models
from django.utils.text import slugify

class Categoria(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    slug = models.SlugField(unique=True, blank=True)  # Permitir que el campo quede vacío inicialmente

    def save(self, *args, **kwargs):
        if not self.slug:  # Generar slug solo si no existe
            base_slug = slugify(self.nombre)
            slug = base_slug
            num = 1
            # Asegurarse de que el slug sea único
            while Categoria.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{num}"
                num += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre
 

# Definir las preguntas frecuentes (FAQ)
class FAQ(models.Model):
    pregunta = models.CharField(max_length=255)
    respuesta = models.TextField()
    categoria = models.ForeignKey(Categoria, related_name="faqs", on_delete=models.CASCADE)

    def __str__(self):
        return self.pregunta










class CertificadoFinalizacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certificados')
    fecha_emision = models.DateTimeField(auto_now_add=True)
    completado = models.BooleanField(default=False)

    def __str__(self):
        return f"Certificado de {self.usuario.username} - {self.fecha_emision.date()}"
    
    
    
   
# Area para mostrar las insigneas de los usuarios 
class Insignia(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='insignias/', null=True, blank=True)

    def __str__(self):
        return self.nombre

# para asignar la insigneas y saber por que 
class InsigniaUsuario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    insignia = models.ForeignKey(Insignia, on_delete=models.CASCADE)
    fecha_otorgada = models.DateTimeField(auto_now_add=True)
    motivo = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.insignia.nombre}"



# area de nitificaciones

from django.contrib.auth.models import User, Group

class Notificacion(models.Model):
    TIPO_DESTINATARIO = [
        ('usuario', 'Usuario'),
        ('grupo', 'Grupo'),
        ('todos', 'Todos'),
    ]

    tipo_destinatario = models.CharField(
        max_length=10,
        choices=TIPO_DESTINATARIO,
        default='usuario'
    )
    usuario = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='notificaciones', 
        blank=True, 
        null=True
    )
    grupo = models.ForeignKey(
        Group, 
        on_delete=models.CASCADE, 
        related_name='notificaciones', 
        blank=True, 
        null=True
    )
    titulo = models.CharField(max_length=255, blank=True, null=True)
    mensaje = models.TextField()
    leido = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo or 'Notificación'} - {self.tipo_destinatario}"
    
    
    
# ----------------------------------------------------------------
# Este modelo registra las lecciones que los usuarios han completado.

from django.db import models
from django.contrib.auth.models import User

class LessonCompletion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.CharField(max_length=255)
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} completed {self.lesson}"





























# Agrega un método clean para validar que los campos correctos se completen en función de tipo_destinatario
from django.core.exceptions import ValidationError

def clean(self):
    if self.tipo_destinatario == 'usuario' and not self.usuario:
        raise ValidationError('Debe especificar un usuario para este tipo de notificación.')
    if self.tipo_destinatario == 'grupo' and not self.grupo:
        raise ValidationError('Debe especificar un grupo para este tipo de notificación.')
    if self.tipo_destinatario == 'todos' and (self.usuario or self.grupo):
        raise ValidationError('No debe especificar usuario o grupo para notificaciones dirigidas a todos.')




# models.py
class VideoEntrenamiento(models.Model):  # Asegúrate de que este sea el nombre exacto
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    archivo_video = models.FileField(upload_to='videos/')

    def __str__(self):
        return self.titulo
    
    
    

# Modelo para manejar la info del perfil del usuario 
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    background_image = models.ImageField(upload_to='backgrounds/', blank=True, null=True)

    def __str__(self):
        return f"Perfil de {self.user.username}"
    




# seccion del sistema de mantenimiento, modelo perteneciente

# models.py

from django.db import models


class Notification(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message[:50]

class SiteConfiguration(models.Model):
    site_name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='site_logo/', null=True, blank=True)
    contact_email = models.EmailField()

    def __str__(self):
        return self.site_name
    
    
# Modelo de planes para check out 
# models.py


class Plan(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    descripcion = models.TextField()
    caracteristicas = models.TextField()

    def __str__(self):
        return self.nombre


    
    

    
    



# Crear el modelo para el blog

# models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from taggit.managers import TaggableManager
from django.core.exceptions import ValidationError



# maneja las categorias de los temas que existen en el blog 

class CategoriaBlog(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre
    
    

# Para garantizar que los campos SEO no excedan los límites recomendados:
# Validación para campos con longitud máxima
from django.core.exceptions import ValidationError

# Definimos la función de validación
from django.core.exceptions import ValidationError

# Definimos la función de validación
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from taggit.managers import TaggableManager
from django.contrib.auth.models import User


# Función de validación para la longitud
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from tinymce.models import HTMLField


# Función de validación para la longitud
def validate_meta_title(value):
    """Valida que el meta_title no supere los 60 caracteres."""
    if len(value) > 60:
        raise ValidationError("El meta título no puede exceder los 60 caracteres.")


def validate_meta_description(value):
    """Valida que el meta_description no supere los 160 caracteres."""
    if len(value) > 160:
        raise ValidationError("La meta descripción no puede exceder los 160 caracteres.")


class BlogPost(models.Model):
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    contenido = HTMLField()  # Cambiado de TextField a HTMLField
    imagen = models.ImageField(upload_to='blog/', blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    publicado = models.BooleanField(default=True)
    categoria = models.ForeignKey(
        'CategoriaBlog',
        on_delete=models.CASCADE,
        related_name='posts',
        null=True,
        blank=True
    )
    tags = TaggableManager()  # Añadir el administrador de etiquetas
    vistas = models.PositiveIntegerField(default=0)  # Nuevo campo para contar las vistas

    # Campos para SEO con validadores explícitos
    meta_title = models.CharField(
        max_length=60,
        validators=[validate_meta_title],  # Validador explícito para meta_title
        blank=True,
        null=True,
        help_text="Título optimizado para SEO. Máximo 60 caracteres."
    )
    meta_description = models.CharField(
        max_length=160,
        validators=[validate_meta_description],  # Validador explícito para meta_description
        blank=True,
        null=True,
        help_text="Descripción optimizada para SEO. Máximo 160 caracteres."
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo

    def contar_reacciones(self, tipo):
        return self.reacciones.filter(tipo=tipo).count()

    def contar_likes(self):
        return self.reacciones.filter(tipo='like').count()

    def contar_loves(self):
        return self.reacciones.filter(tipo='love').count()
    
    
    
    def get_absolute_url(self):
        return reverse('detalle_blog', args=[self.slug])

    def get_share_urls(self):
        base_url = f"{self.get_absolute_url()}"
        full_url = f"{settings.SITE_URL}{base_url}"
        return {
            'facebook': f"https://www.facebook.com/sharer/sharer.php?u={full_url}",
            'twitter': f"https://twitter.com/intent/tweet?url={full_url}&text={self.titulo}",
            'linkedin': f"https://www.linkedin.com/shareArticle?mini=true&url={full_url}&title={self.titulo}",
            'whatsapp': f"https://api.whatsapp.com/send?text={full_url}",
        }





    
    
    
    
    
    
    
    
    
    
    
# Modelo para manejar comentarios 

# models.py
from django.db import models
from django.contrib.auth.models import User

class Comentario(models.Model):
    post = models.ForeignKey('BlogPost', on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comentarios')
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    aprobado = models.BooleanField(default=True)
    voto_positivo = models.PositiveIntegerField(default=0)
    voto_negativo = models.PositiveIntegerField(default=0)
    padre = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='respuestas')
    

    def __str__(self):
        return f"{self.autor.username} - {self.contenido[:20]}"




#  Modelo de Suscripción 

# models.py
from django.db import models

class Suscriptor(models.Model):
    email = models.EmailField(unique=True)
    fecha_suscripcion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email



#  Añade un modelo para registrar los "Me gusta" o "Me encanta". 

# models.py
from django.db import models
from django.contrib.auth.models import User

class Reaccion(models.Model):
    TIPOS_REACCION = [
        ('like', 'Me gusta'),
        ('love', 'Me encanta'),
    ]

    post = models.ForeignKey('BlogPost', on_delete=models.CASCADE, related_name='reacciones')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo = models.CharField(choices=TIPOS_REACCION, max_length=10)

    class Meta:
        unique_together = ('post', 'usuario')  # Un usuario solo puede reaccionar una vez a un post




# Configurar la Notificación al Publicar
from django.core.mail import send_mass_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import BlogPost, Suscriptor

@receiver(post_save, sender=BlogPost)
def notificar_suscriptores(sender, instance, created, **kwargs):
    if created and instance.publicado:  # Notificar solo si es una nueva publicación y está publicada
        suscriptores = Suscriptor.objects.all()
        correos = [s.email for s in suscriptores]

        if correos:
            mensaje = (
                f"¡Nueva publicación en el blog: {instance.titulo}!",
                f"Hola,\n\nSe ha publicado un nuevo artículo en nuestro blog: {instance.titulo}.\n"
                f"Puedes leerlo aquí: https://tusitio.com/blog/{instance.slug}\n\n¡Gracias por seguirnos!",
                "no-reply@tusitio.com",
                correos
            )
            send_mass_mail((mensaje,), fail_silently=False)



