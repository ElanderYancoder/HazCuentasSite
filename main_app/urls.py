from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .views import panel_retroalimentaciones


urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('ayuda', views.ayuda, name='ayuda'),
    path('ayuda/', views.centro_ayuda, name='ayuda'),
    path('ayuda/<slug:slug>/', views.preguntas_por_categoria, name='categoria_ayuda'),
    path('agregar-faq/', views.agregar_faq, name='agregar_faq'),
    path('panel-retroalimentaciones/', panel_retroalimentaciones, name='panel_retroalimentaciones'),
    path('editar-retroalimentacion/<int:pk>/', views.editar_retroalimentacion, name='editar_retroalimentacion'),
    path('eliminar-retroalimentacion/<int:pk>/', views.eliminar_retroalimentacion, name='eliminar_retroalimentacion'),
    path('noticias/', views.noticias, name='noticias'),
    path('noticias/', views.lista_noticias, name='lista_noticias'),
    path('noticias/<int:id>/', views.detalle_noticia, name='detalle_noticia'),
    path('registro/', views.registro, name='registro'),
    path('login/', auth_views.LoginView.as_view(template_name='main_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('entrenamiento/', views.entrenamiento, name='entrenamiento'),
    path('entrenamiento/lista/', views.lista_entrenamiento, name='lista_entrenamiento'),
    path('entrenamiento/leccion/<int:leccion_id>/', views.detalle_leccion, name='detalle_leccion'),
    path('entrenamiento/progreso/', views.progreso_entrenamiento, name='progreso_entrenamiento'),
    path('historial-progreso/', views.historial_progreso, name='historial_progreso'),
    path('marcar_completada/<int:leccion_id>/', views.marcar_como_completada, name='marcar_completada'),
    path('leccion/<int:leccion_id>/', views.detalle_leccion, name='detalle_leccion'),
    path('leccion/<int:leccion_id>/retroalimentacion/', views.agregar_retroalimentacion, name='agregar_retroalimentacion'),
    path('certificado/<int:certificado_id>/descargar/', views.descargar_certificado, name='descargar_certificado'),
    path('certificado/descargar/', views.descargar_certificado, name='descargar_certificado'),
    path('mis-insignias/', views.mis_insignias, name='mis_insignias'),
    path('otorgar-insignia/', views.otorgar_insignia, name='otorgar_insignia'),
    path('crear-insignia/', views.crear_insignia, name='crear_insignia'),
    path('gestionar-insignias/', views.gestionar_insignias, name='gestionar_insignias'),
    path('editar-insignia/<int:pk>/', views.editar_insignia, name='editar_insignia'),
    path('eliminar-insignia/<int:pk>/', views.eliminar_insignia, name='eliminar_insignia'),
    path('notificaciones/', views.notificaciones, name='notificaciones'),
    path('notificaciones/marcar/<int:notificacion_id>/', views.marcar_notificacion_como_leida, name='marcar_notificacion_como_leida'),
    path('notificaciones/marcar-todas/', views.marcar_todas_notificaciones_como_leidas, name='marcar_todas_notificaciones_como_leidas'),
    path('notificaciones/eliminar/<int:notificacion_id>/', views.eliminar_notificacion, name='eliminar_notificacion'),
    path('notificaciones/prueba/', views.enviar_notificacion_prueba, name='enviar_notificacion_prueba'), # pueba luego sera eliminada 
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
    path('plan-basic/', views.plan_basic, name='plan_basic'),
    path('plan-professional/', views.plan_professional, name='plan_professional'),
    path('plan-enterprise/', views.plan_enterprise, name='plan_enterprise'),
    path('suscripcion/', views.subscribe, name='suscripcion'),
    path('suscripcion-exitosa/', views.subscription_success, name='subscription_success'),  # Página de éxito después de la suscripción
    path('testimonios/', views.testimonios, name='testimonios'),
    path('agregar-testimonio/', views.agregar_testimonio, name='agregar_testimonio'),
    path('moderar-testimonios/', views.moderar_testimonios, name='moderar_testimonios'),
    path('cambiar_estado_testimonio/<int:pk>/', views.cambiar_estado_testimonio, name='cambiar_estado_testimonio'),
    # Blog space 
    path('blog/', views.lista_blog, name='lista_blog'),  # Página de inicio del blog
    path('blog/categoria/<slug:slug>/', views.lista_blog, name='categoria_blog'),  # Filtrar por categoría
    path('blog/<slug:slug>/', views.detalle_blog, name='detalle_blog'),  # Detalle de una publicación
    path('comentario/<int:comentario_id>/votar/<str:tipo>/', views.votar_comentario, name='votar_comentario'),
    # Rutas para votar y responder comentarios
    path('comentarios/<int:comentario_id>/votar/<str:voto>/', views.votar_comentario, name='votar_comentario'),
    path('comentarios/<int:comentario_id>/responder/', views.responder_comentario, name='responder_comentario'),
    # Politicas terminos y condiciones 
    path('politica-privacidad/', views.politica_de_privacidad, name='politica_privacidad'),
    path('terminos-condiciones/', views.terminos_y_condiciones, name='terminos_condiciones'),
    # reacciones del blog 
    path('reaccionar/<int:post_id>/<str:tipo>/', views.reaccionar, name='reaccionar'),
    # suscripciones 
    path('suscribirse/', views.suscribirse, name='suscribirse'),
    # contactos seccion de ayuda 
    path('contacto/', views.contacto, name='contacto'),
    
    
  
]

# urls.py onfiguración para servir archivos multimedia durante el desarrollo:
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




# Vista de registro
def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Tu cuenta ha sido creada exitosamente! Ahora puedes iniciar sesión.')
            return redirect('login')
        else:
            # Mensaje de error si el formulario no es válido
            messages.error(request, 'Hubo un error en el formulario. Por favor, revisa los campos.')
    else:
        form = UserCreationForm()

    return render(request, 'main_app/registro.html', {'form': form})








'''Nota
Esta configuración solo debería usarse en entornos de desarrollo. 
En producción, la gestión de archivos estáticos y multimedia debe
hacerse a través de un servidor web como Nginx o mediante un servicio
de almacenamiento en la nube.'''
# Añadir la configuración de archivos estáticos y multimedia
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)