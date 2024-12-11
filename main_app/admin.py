from django.contrib import admin

# Register your models here.
# admin.py

from django.contrib import admin
from django.shortcuts import render
from .models import  Notification, SiteConfiguration


admin.site.register(Notification)
admin.site.register(SiteConfiguration)


# admin.py
from django.contrib import admin
from .models import Leccion

class LeccionAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'descripcion', 'imagen')
    search_fields = ('titulo',)
    list_filter = ('titulo',)
    # Incluir el campo de video en el formulario de administración
    fields = ('titulo', 'descripcion', 'contenido', 'video')

admin.site.register(Leccion, LeccionAdmin)




# admin sesion para subir las noticias 
from django.contrib import admin
from .models import Noticia

@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'fecha_publicacion', 'destacado')
    list_filter = ('fecha_publicacion', 'destacado')
    search_fields = ('titulo', 'contenido')
    prepopulated_fields = {'titulo': ('titulo',)}  # Para generar slugs automáticamente




# ----------------------------------------------------------------
# testimonios 
# admin.py
from django.contrib import admin
from .models import Testimonio

class TestimonioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'comentario', 'estado', 'fecha_creacion')
    list_filter = ('estado',)
    actions = ['aprobar_testimonios', 'rechazar_testimonios']

    def aprobar_testimonios(self, request, queryset):
        queryset.update(estado='aprobado')
    aprobar_testimonios.short_description = 'Aprobar testimonios seleccionados'

    def rechazar_testimonios(self, request, queryset):
        queryset.update(estado='rechazado')
    rechazar_testimonios.short_description = 'Rechazar testimonios seleccionados'

admin.site.register(Testimonio, TestimonioAdmin)


# ----------------------------------------------------------------
# admin para agrega preguntas frecuentes 

from django.contrib import admin
from .models import FAQ, Categoria

# Configurar la visualización de FAQ
class FAQAdmin(admin.ModelAdmin):
    list_display = ('pregunta', 'categoria')  # Muestra la pregunta y la categoría en la lista
    search_fields = ('pregunta', 'respuesta')  # Agrega un buscador para las preguntas y respuestas
    list_filter = ('categoria',)  # Agrega un filtro por categorías

# Configurar la visualización de Categorías
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')  # Muestra el nombre y la descripción en la lista
    search_fields = ('nombre', 'descripcion')  # Agrega un buscador para categorías

# Registrar los modelos en el panel de administración
admin.site.register(FAQ, FAQAdmin)
admin.site.register(Categoria, CategoriaAdmin)

# ----------------------------------------------------------------
# para administrar las notificaciones 
from django.contrib import admin
from .models import Notificacion

@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo_destinatario', 'usuario', 'grupo', 'leido', 'fecha_creacion')
    list_filter = ('tipo_destinatario', 'leido', 'fecha_creacion')
    search_fields = ('titulo', 'mensaje', 'usuario__username', 'grupo__name')
    


# sesion para aprobar los comentarios 
# admin.py
from django.contrib import admin
from django.contrib.auth.models import User
from .models import BlogPost, Comentario, Notificacion

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('autor', 'post', 'fecha_creacion', 'aprobado')
    list_filter = ('aprobado', 'fecha_creacion')
    search_fields = ('autor__username', 'contenido')
    actions = ['aprobar_comentarios']

    def aprobar_comentarios(self, request, queryset):
        comentarios_aprobados = queryset.filter(aprobado=False)
        for comentario in comentarios_aprobados:
            comentario.aprobado = True
            comentario.save()

            # Crear la notificación
            mensaje = f"Tu comentario en '{comentario.post.titulo}' ha sido aprobado."
            Notificacion.objects.create(
                usuario=comentario.autor,
                mensaje=mensaje,
            )
        self.message_user(request, "Comentarios aprobados y notificaciones enviadas.")
    aprobar_comentarios.short_description = 'Aprobar comentarios seleccionados'


# =================================================================
# Panel para manejas la categorias de los temas del blos 
# admin.py
from django.contrib import admin
from .models import BlogPost, CategoriaBlog
from django.contrib import admin
from .models import BlogPost
from .forms import BlogPostAdminForm


from django.contrib import admin
from django.db.models import Count
from .models import BlogPost, CategoriaBlog

@admin.register(CategoriaBlog)
class CategoriaBlogAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'slug')
    prepopulated_fields = {'slug': ('nombre',)}
    search_fields = ('nombre', 'descripcion')

from django.urls import path, reverse
from django.utils.html import format_html
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render
import csv

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    # Configuración de la lista
    list_display = (
        'titulo', 'autor', 'vistas', 'comentarios_count', 
        'categoria', 'publicado', 'fecha_creacion', 'estadisticas_link'
    )
    list_filter = ('categoria', 'publicado', 'tags', 'fecha_creacion')
    search_fields = ('titulo', 'contenido', 'meta_title', 'meta_description')
    ordering = ('-fecha_creacion', 'titulo')

    # Configuración de campos en el formulario
    fields = (
        'titulo', 'slug', 'contenido', 'imagen', 'categoria', 'tags',
        'publicado', 'vistas', 'meta_title', 'meta_description', 'fecha_creacion'
    )
    readonly_fields = ('vistas', 'fecha_creacion', 'fecha_actualizacion')

    # Acciones personalizadas
    actions = ['exportar_a_csv']

    # Función para mostrar el conteo de comentarios
    def comentarios_count(self, obj):
        return obj.comentarios.count()

    comentarios_count.short_description = "Comentarios"

    # Exportar publicaciones a CSV
    def exportar_a_csv(self, request, queryset):
        """Exportar publicaciones seleccionadas a un archivo CSV."""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="blog_posts.csv"'

        writer = csv.writer(response)
        writer.writerow([
            'Título', 'Autor', 'Vistas', 'Comentarios', 'Categoría',
            'Publicado', 'Fecha de Creación', 'Meta Título', 'Meta Descripción'
        ])

        for post in queryset.annotate(comments_count=Count('comentarios')):
            writer.writerow([
                post.titulo, post.autor.username, post.vistas, post.comments_count,
                post.categoria.nombre if post.categoria else '',
                post.publicado, post.fecha_creacion, post.meta_title, post.meta_description
            ])

        self.message_user(request, "Exportación a CSV completada exitosamente.")
        return response

    exportar_a_csv.short_description = "Exportar publicaciones seleccionadas a CSV"

    # Botón para acceder a las estadísticas
    def estadisticas_link(self, obj):
        url = reverse('admin:blogpost_estadisticas')
        return format_html('<a class="button" href="{}">Ver Estadísticas</a>', url)

    estadisticas_link.short_description = "Estadísticas"
    estadisticas_link.allow_tags = True

    # Añadir la URL personalizada para estadísticas
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'estadisticas/',
                self.admin_site.admin_view(self.blog_statistics),
                name='blogpost_estadisticas'
            ),
        ]
        return custom_urls + urls

    # Vista de estadísticas
    def blog_statistics(self, request):
        """Renderizar la página de estadísticas del blog."""
        posts = BlogPost.objects.all()
        data = {
            "labels": [post.titulo for post in posts],
            "vistas": [post.vistas for post in posts],
            "comentarios": [post.comentarios.count() for post in posts],
        }
        return render(request, 'admin/blog_statistics.html', {'data': data})









    
        


# Configurar el Administrador de BlogPost 

from django.contrib import admin
from django.db.models import Count
from django.urls import path
from django.template.response import TemplateResponse
from .models import BlogPost

class BlogStatisticsAdmin(admin.ModelAdmin):
    change_list_template = "admin/blog_statistics.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('statistics/', self.admin_site.admin_view(self.statistics_view), name="blog_statistics"),
        ]
        return custom_urls + urls

    def statistics_view(self, request):
        # Datos para el gráfico
        posts_data = BlogPost.objects.annotate(
            comments_count=Count('comentarios')
        ).values('titulo', 'vistas', 'comments_count')

        # Preparar datos para Chart.js
        chart_data = {
            "labels": [post['titulo'] for post in posts_data],
            "vistas": [post['vistas'] for post in posts_data],
            "comentarios": [post['comments_count'] for post in posts_data],
        }

        context = {
            "chart_data": chart_data,
            "opts": self.model._meta,
        }
        return TemplateResponse(request, "admin/blog_statistics.html", context)





