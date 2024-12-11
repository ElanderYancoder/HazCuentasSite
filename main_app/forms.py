from django import forms
from .models import Retroalimentacion
from .models import Leccion
from django import forms
from .models import VideoEntrenamiento, Notification, SiteConfiguration 




# formulario para que el usuario pueda dejar su comentario 

class RetroalimentacionForm(forms.ModelForm):
    class Meta:
        model = Retroalimentacion
        fields = ['comentario', 'calificacion']
        widgets = {
            'comentario': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'calificacion': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'comentario': 'Escribe tu comentario:',
            'calificacion': 'Calificación:',
        }






# Formulario para subir los video 


class VideoLeccionForm(forms.ModelForm):
    class Meta:
        model = VideoEntrenamiento  # Asegúrate de que el modelo coincida
        fields = ['titulo', 'descripcion', 'archivo_video']  # Debe ser `archivo_video`, no `video`
        
    
    
# formulario para manejar la info del usuario 

# forms.py
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from .models import Profile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class UpdateBackgroundForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['background_image']  # Este campo se debe agregar en el modelo Profile

class UpdatePasswordForm(PasswordChangeForm):
    pass



# seccion de mantenimiento de la pagina 

# forms.py





class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['message']

class SiteConfigurationForm(forms.ModelForm):
    class Meta:
        model = SiteConfiguration
        fields = ['site_name', 'logo', 'contact_email']




# formulario para que los administradores puedan otorgar las insigneas 

from django import forms
from .models import InsigniaUsuario

class OtorgarInsigniaForm(forms.ModelForm):
    class Meta:
        model = InsigniaUsuario
        fields = ['usuario', 'insignia', 'motivo']
 


# Formulario para Subir Imágenes 

from django import forms
from .models import Insignia

class InsigniaForm(forms.ModelForm):
    class Meta:
        model = Insignia
        fields = ['nombre', 'descripcion', 'imagen']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la insignia'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción'}),
        }
        labels = {
            'nombre': 'Nombre',
            'descripcion': 'Descripción',
            'imagen': 'Imagen de la Insignia',
        }


# ----------------------------------------------------------------
# fpormulario de testimonios 

# forms.py
from django import forms
from .models import Testimonio

class TestimonioForm(forms.ModelForm):
    class Meta:
        model = Testimonio
        fields = ['nombre', 'puesto','comentario', 'foto', 'enlace_redes']
        labels = {
            'comentario': 'Tu Testimonio',
            'foto': 'Foto de Perfil',
            'enlace_redes': 'Enlace a tu página web o redes sociales',
        }
        widgets = {
            'comentario': forms.Textarea(attrs={'rows': 4}),
            'enlace_redes': forms.URLInput(attrs={'placeholder': 'Ejemplo: https://www.linkedin.com/in/tu-perfil'}),
        }

    # Validación personalizada si es necesario
    def clean_comentario(self):
        comentario = self.cleaned_data.get('comentario')
        if len(comentario) < 10:
            raise forms.ValidationError('El testimonio debe tener al menos 10 caracteres.')
        return comentario


# ----------------------------------------------------------------
# formulario de preguntas frecuentes 

from django import forms
from .models import FAQ

class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ['pregunta', 'respuesta', 'categoria']
        widgets = {
            'pregunta': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escribe la pregunta'}),
            'respuesta': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escribe la respuesta'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
        }




# Comentarios del blog 
# forms.py
from django import forms
from .models import Comentario

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['contenido']
        widgets = {
            'contenido': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Escribe tu comentario aquí...'}),
        }
        labels = {
            'contenido': '',
        }



# Formulario de Suscripción
from django import forms
from .models import Suscriptor

class SuscripcionForm(forms.ModelForm):
    class Meta:
        model = Suscriptor
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingresa tu correo electrónico...'
            })
        }
        





# Personalizado para BlogPostAdmin 
from django import forms
from tinymce.widgets import TinyMCE
from .models import BlogPost

class BlogPostAdminForm(forms.ModelForm):
    """
    Formulario personalizado para BlogPost en el panel de administración,
    usando CKEditor para el campo 'contenido'.
    """
    contenido = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))


    class Meta:
        model = BlogPost
        fields = [
            'titulo',
            'slug',
            'autor',
            'contenido',
            'imagen',
            'categoria',
            'tags',
            'vistas',
            'publicado',
            'meta_title',
            'meta_description',
        ]



# Define un formulario para capturar los datos del usuario.

from django import forms

class ContactForm(forms.Form):
    nombre = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Tu nombre'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Tu correo electrónico'
    }))
    mensaje = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Tu mensaje',
        'rows': 5
    }))
