from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.timezone import now

from main_app.utils import otorgar_insignia_por_curso
from .models import Leccion, ProgresoUsuario, Noticia, Retroalimentacion, CertificadoFinalizacion, Insignia, InsigniaUsuario, Notificacion
from .forms import ComentarioForm, RetroalimentacionForm
from reportlab.pdfgen import canvas
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors 
from django.urls import reverse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.core.paginator import Paginator
from .forms import VideoLeccionForm, NotificationForm, SiteConfigurationForm
from .models import  SiteConfiguration
from django.contrib.auth.decorators import user_passes_test











# Vista principal
def home(request):
    return render(request, "main_app/home.html")


# pagina acerca de 
def about(request):
    valores = [
        {"title": "Innovación", "text": "Siempre estamos buscando nuevas formas de mejorar nuestros servicios y herramientas para ofrecer soluciones más eficientes."},
        {"title": "Compromiso", "text": "Nos comprometemos a brindar un excelente servicio y soporte, buscando siempre la satisfacción y éxito de nuestros clientes."},
        {"title": "Transparencia", "text": "Mantenemos una comunicación abierta y clara con nuestros clientes, garantizando procesos transparentes y efectivos."},
    ]
    equipo = [
        {"img": "team-member-1.webp", "name": "Juan Pérez", "role": "CEO y Fundador"},
        {"img": "team-member-2.webp", "name": "Ana Gómez", "role": "Directora de Tecnología"},
        {"img": "team-member-3.webp", "name": "Carlos Fernández", "role": "Director de Marketing"},
    ]

    return render(request, "main_app/about.html" , {"valores": valores, "equipo": equipo})

def ayuda(request):
    return render(request, "main_app/ayuda.html")




# politica de privacidad 
def politica_de_privacidad(request):
    return render(request, "main_app/politica_privacidad.html")

# Terminos y condiciones 
def terminos_y_condiciones(request):
    return render(request, "main_app/terminos_condiciones.html")

# Vista para noticias
def noticias(request):
    noticias = Noticia.objects.all()
    return render(request, 'main_app/noticias.html', {'noticias': noticias})

# Vista de detalle de una noticia específica
from django.shortcuts import render, get_object_or_404
from .models import Noticia

def detalle_noticia(request, id):
    noticia = get_object_or_404(Noticia, id=id)
    return render(request, 'main_app/detalle_noticia.html', {'noticia': noticia})




# Lista de noticias 
from django.shortcuts import render
from .models import Noticia

from django.core.paginator import EmptyPage, PageNotAnInteger

def lista_noticias(request):
    noticias_list = Noticia.objects.order_by('-fecha_publicacion')
    paginator = Paginator(noticias_list, 5)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)  # Mostrar la primera página
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)  # Mostrar la última página
    
    return render(request, 'main_app/lista_noticias.html', {'page_obj': page_obj})





# Vista para el registro de usuarios
def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Tu cuenta ha sido creada exitosamente!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'main_app/registro.html', {'form': form})

# Vista de la página de inicio de entrenamiento
@login_required
def entrenamiento(request):
    return render(request, 'main_app/entrenamiento.html')

@login_required
def lista_entrenamiento(request):
    # Obtener todas las lecciones y el progreso del usuario actual
    lecciones = Leccion.objects.all()
    progreso = ProgresoUsuario.objects.filter(usuario=request.user)
    lecciones_completadas = [p.leccion.id for p in progreso if p.completado]

    # Verificar si el usuario ha completado todas las lecciones
    total_lecciones = lecciones.count()
    count_lecciones_completadas = len(lecciones_completadas)

    if count_lecciones_completadas == total_lecciones:
        # Crear o encontrar la insignia de "Curso Completado"
        insignia, created = Insignia.objects.get_or_create(
            nombre="Curso Completado",
            descripcion="Has completado todas las lecciones."
        )

        # Verificar si el usuario ya tiene la insignia; si no, asignarla
        if not InsigniaUsuario.objects.filter(usuario=request.user, insignia=insignia).exists():
            InsigniaUsuario.objects.create(usuario=request.user, insignia=insignia)
            
            # Crear una notificación para informar al usuario
            Notificacion.objects.create(
                usuario=request.user,
                mensaje="¡Felicidades! Has completado todas las lecciones del curso."
            )

    # Pasar los datos necesarios a la plantilla
    context = {
        'lecciones': lecciones,
        'lecciones_completadas': lecciones_completadas,
    }
    
    return render(request, 'main_app/lista_entrenamiento.html', context)
    
    

# Funcion para marca la leccion como completada 
from django.utils.timezone import now  # Asegúrate de importar correctamente
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required


@login_required
def marcar_como_completada(request, leccion_id):
    leccion = get_object_or_404(Leccion, id=leccion_id)
    
    progreso, created = ProgresoUsuario.objects.get_or_create(
        usuario=request.user,
        leccion=leccion,
    )
    
    
    print(f"Antes de modificar: completado={progreso.completado}, fecha_completado={progreso.fecha_completado}")

    if created or not progreso.completado:
        progreso.completado = True
        progreso.fecha_completado = now()
        otorgar_insignia_por_curso(request.user, leccion)
        
        #print(f"Fecha generada por now(): {now()}")  # Asegúrate de que no sea None

        progreso.save()

        
        # Crear notificación
        Notificacion.objects.create(
            usuario=request.user,
            titulo="¡Lección completada!",
            mensaje=f"Has completado la lección '{leccion.titulo}'. ¡Sigue así!"
        )

        # Enviar notificación en tiempo real
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"user_{request.user.id}",
            {
                "type": "send_notification",
                "title": "¡Lección completada!",
                "message": f"Has completado la lección '{leccion.titulo}'. ¡Sigue así!"
            }
        )

        
    return redirect('lista_entrenamiento')






# ----------------------------------------------------------------
# Funcion para enviar notificacion a los clientes 





# Vista para los detalles de una lección individual
@login_required
def detalle_leccion(request, leccion_id):
    # Obtener la lección y el progreso del usuario
    leccion = get_object_or_404(Leccion, id=leccion_id)
    progreso, created = ProgresoUsuario.objects.get_or_create(usuario=request.user, leccion=leccion)
    completado = progreso.completado

    # Inicializar el formulario fuera del flujo condicional
    form = None

    # Procesar el formulario de retroalimentación
    if request.method == 'POST':
        if 'submit_feedback' in request.POST:
            form = RetroalimentacionForm(request.POST)
            if form.is_valid():
                retroalimentacion = form.save(commit=False)
                retroalimentacion.usuario = request.user
                retroalimentacion.leccion = leccion
                retroalimentacion.fecha = timezone.now()
                retroalimentacion.save()
                messages.success(request, '¡Gracias por tu retroalimentación!')
                return redirect('detalle_leccion', leccion_id=leccion.id)
        elif not completado:
            # Marcar como completada si aún no lo está
            progreso.completado = True
            progreso.fecha_completado = timezone.now()  # Aseguramos guardar la fecha actual
            progreso.save()
            messages.success(request, '¡Lección marcada como completada!')
            return redirect('progreso_entrenamiento')
    else:
        form = RetroalimentacionForm()

    # Obtener las retroalimentaciones de esta lección
    retroalimentaciones = Retroalimentacion.objects.filter(leccion=leccion).order_by('-fecha')

    return render(request, 'main_app/detalle_leccion.html', {
        'leccion': leccion,
        'completado': completado,
        'form': form,
        'retroalimentaciones': retroalimentaciones,
    })





# vista para el formulario de retroalimentacion 
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Retroalimentacion
from .forms import RetroalimentacionForm

class RetroalimentacionCreateView(CreateView):
    model = Retroalimentacion
    form_class = RetroalimentacionForm

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        form.instance.leccion_id = self.kwargs['leccion_id']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('detalle_leccion', kwargs={'pk': self.kwargs['leccion_id']})
    
    
    
    
# ----------------------------------------------------------------
# agregar vista para retroalimentacion 

@login_required
def agregar_retroalimentacion(request, leccion_id):
    # Obtener la lección a la que se asociará la retroalimentación
    leccion = get_object_or_404(Leccion, id=leccion_id)
    
    if request.method == 'POST':
        form = RetroalimentacionForm(request.POST)
        if form.is_valid():
            # Guardar la retroalimentación
            retroalimentacion = form.save(commit=False)
            retroalimentacion.usuario = request.user
            retroalimentacion.leccion = leccion
            retroalimentacion.fecha = timezone.now()
            retroalimentacion.save()
            
            # Mensaje de éxito y redirección
            messages.success(request, '¡Gracias por tu retroalimentación!')
            return redirect('detalle_leccion', leccion_id=leccion.id)
    else:
        form = RetroalimentacionForm()

    return render(request, 'agregar_retroalimentacion.html', {
        'leccion': leccion,
        'form': form,
    })




# Panel de administracion para gestionar las restroalimentaciones 
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Avg
from .models import Retroalimentacion

@staff_member_required # decorador para solo permitir el acceso si el usuario es miebra de la admihnistracion 
def panel_retroalimentaciones(request):
    # Validar que el usuario es staff
    if not request.user.is_staff:
        return render(request, '403.html', status=403)

    # Obtener retroalimentaciones ordenadas por fecha
    retroalimentaciones = Retroalimentacion.objects.all().order_by('-fecha')

    # Filtrar por búsqueda
    query = request.GET.get('q', '')
    if query:
        retroalimentaciones = retroalimentaciones.filter(
            comentario__icontains=query
        )

    # Calcular estadísticas generales
    promedio_calificaciones = retroalimentaciones.aggregate(promedio=Avg('calificacion'))['promedio']

    # Paginación
    paginator = Paginator(retroalimentaciones, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Renderizar la plantilla
    return render(request, 'panel_retroalimentaciones.html', {
        'retroalimentaciones': page_obj,
        'promedio_calificaciones': promedio_calificaciones,
        'query': query,
    })

# opcion editar la restroalimentacion 
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Retroalimentacion
from .forms import RetroalimentacionForm

@staff_member_required
def editar_retroalimentacion(request, pk):
    retroalimentacion = get_object_or_404(Retroalimentacion, pk=pk)
    
    if request.method == "POST":
        form = RetroalimentacionForm(request.POST, instance=retroalimentacion)
        if form.is_valid():
            form.save()
            messages.success(request, "Retroalimentación actualizada correctamente.")
            return redirect('panel_retroalimentaciones')
    else:
        form = RetroalimentacionForm(instance=retroalimentacion)
    
    return render(request, 'editar_retroalimentacion.html', {'form': form, 'retroalimentacion': retroalimentacion})


# opcion para la eliminacion de la retroalimentacion  
@staff_member_required
def eliminar_retroalimentacion(request, pk):
    retroalimentacion = get_object_or_404(Retroalimentacion, pk=pk)
    
    if request.method == "POST":
        retroalimentacion.delete()
        messages.success(request, "Retroalimentación eliminada correctamente.")
        return redirect('panel_retroalimentaciones')
    
    return render(request, 'eliminar_retroalimentacion.html', {'retroalimentacion': retroalimentacion})





# Vista para el progreso de entrenamiento del usuario
@login_required
def progreso_entrenamiento(request):
    lecciones = Leccion.objects.all()
    progreso_usuario = ProgresoUsuario.objects.filter(usuario=request.user, completado=True)

    lecciones_completadas = [progreso.leccion for progreso in progreso_usuario]
    lecciones_pendientes = lecciones.exclude(id__in=[l.id for l in lecciones_completadas])

    total_lecciones = lecciones.count()
    total_completadas = progreso_usuario.count()
    total_pendientes = total_lecciones - total_completadas

    porcentaje_completado = (total_completadas / total_lecciones * 100) if total_lecciones > 0 else 0

    context = {
        'lecciones': lecciones,
        'lecciones_completadas': lecciones_completadas,
        'lecciones_pendientes': lecciones_pendientes,
        'porcentaje_completado': porcentaje_completado,
        'total_completadas': total_completadas,
        'total_pendientes': total_pendientes,
    }
    return render(request, 'main_app/progreso_entrenamiento.html', context)




@login_required
def historial_progreso(request):
    # Obtiene el progreso del usuario, filtrando las lecciones completadas
    progreso_completado = ProgresoUsuario.objects.filter(usuario=request.user, completado=True).order_by('-fecha_completado')
    
    # Debug temporal
    """for progreso in progreso_completado:
        print(progreso.fecha_completado)  # Verifica que las fechas sean correctas"""

    
    return render(request, 'main_app/historial_progreso.html', {
        'progreso_completado': progreso_completado,
    })
    

 

def verificar_certificado(request):
    # Contar todas las lecciones y las completadas por el usuario
    total_lecciones = Leccion.objects.count()
    completadas = ProgresoUsuario.objects.filter(usuario=request.user, completado=True).count()

    # Si todas las lecciones están completas y el usuario aún no tiene un certificado, generarlo
    if completadas == total_lecciones and not CertificadoFinalizacion.objects.filter(usuario=request.user, completado=True).exists():
        CertificadoFinalizacion.objects.create(usuario=request.user, completado=True)


@login_required
def ver_certificado(request):
    certificado = get_object_or_404(CertificadoFinalizacion, usuario=request.user, completado=True)
    return render(request, 'main_app/ver_certificado.html', {'certificado': certificado})





# Area de descarga del certificado 
@login_required
def descargar_certificado(request):
    # Cargar el certificado del usuario
    certificado = get_object_or_404(CertificadoFinalizacion, usuario=request.user)

    # Crear la respuesta HTTP con el tipo de contenido PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="certificado_finalizacion.pdf"'

    # Crear el objeto canvas
    pdf_canvas = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Establecer colores y fuentes
    title_color = colors.HexColor("#004aad")
    text_color = colors.black

    # Dibujar el título del certificado
    pdf_canvas.setFont("Helvetica-Bold", 28)
    pdf_canvas.setFillColor(title_color)
    pdf_canvas.drawCentredString(width / 2, height - 100, "Certificado de Finalización")

    # Dibujar el subtítulo
    pdf_canvas.setFont("Helvetica", 16)
    pdf_canvas.setFillColor(text_color)
    pdf_canvas.drawCentredString(width / 2, height - 150, "Este certificado es otorgado a")

    # Dibujar el nombre del usuario en el centro
    pdf_canvas.setFont("Helvetica-Bold", 22)
    pdf_canvas.drawCentredString(width / 2, height - 200, certificado.usuario.get_full_name())

    # Mensaje de finalización
    pdf_canvas.setFont("Helvetica", 16)
    pdf_canvas.drawCentredString(width / 2, height - 250, "por haber completado exitosamente el curso de")

    pdf_canvas.setFont("Helvetica-Bold", 18)
    pdf_canvas.drawCentredString(width / 2, height - 280, "Digitalización de Negocios")

    # Fecha de emisión, usando el atributo fecha_emision del certificado
    pdf_canvas.setFont("Helvetica-Oblique", 12)
    fecha_emision = certificado.fecha_emision.strftime('%d %B %Y')
    pdf_canvas.drawCentredString(width / 2, height - 330, f"Fecha de emisión: {fecha_emision}")

    # Firma o espacio para una firma (opcional)
    pdf_canvas.setFont("Helvetica", 14)
    pdf_canvas.drawString(100, height - 500, "_____________________")
    pdf_canvas.drawString(100, height - 520, "Firma del Instructor")

    pdf_canvas.setFont("Helvetica", 14)
    pdf_canvas.drawString(width - 250, height - 500, "_____________________")
    pdf_canvas.drawString(width - 250, height - 520, "Fecha de Aprobación")

    # Finalizar y guardar el PDF
    pdf_canvas.showPage()
    pdf_canvas.save()

    return response




# ----------------------------------------------------------------
# Asignear insigneas 

from django import forms
from .models import InsigniaUsuario

class OtorgarInsigniaForm(forms.ModelForm):
    class Meta:
        model = InsigniaUsuario
        fields = ['usuario', 'insignia', 'motivo']


# area de insigneas 
@login_required
def mis_insignias(request):
    insignias_usuario = InsigniaUsuario.objects.filter(usuario=request.user)
    return render(request, 'main_app/mis_insignias.html', {'insignias_usuario': insignias_usuario})


# Otorgar insignias (solo administradores)
@user_passes_test(lambda u: u.is_staff)
def otorgar_insignia(request):
    if request.method == 'POST':
        form = OtorgarInsigniaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('otorgar_insignia')
    else:
        form = OtorgarInsigniaForm()
    return render(request, 'otorgar_insignia.html', {'form': form})



# Vista para Gestionar el Formulario de subir la imagenes de las insigneas 
from django.shortcuts import render, redirect
from .forms import InsigniaForm
from django.contrib import messages

def crear_insignia(request):
    if request.method == 'POST':
        form = InsigniaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Insignia creada exitosamente.')
            return redirect('crear_insignia')  # Cambiar por la URL adecuada.
        else:
            messages.error(request, 'Hubo un error al crear la insignia.')
    else:
        form = InsigniaForm()
    return render(request, 'entrenamiento/crear_insignia.html', {'form': form})


# Agrega las vistas correspondientes para gestionar, editar y eliminar insignias:

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import Insignia
from .forms import InsigniaForm

# Vista para gestionar insignias
@staff_member_required
def gestionar_insignias(request):
    insignias = Insignia.objects.all()
    return render(request, 'entrenamiento/gestionar_insignias.html', {'insignias': insignias})

# Vista para editar una insignia
@staff_member_required
def editar_insignia(request, pk):
    insignia = get_object_or_404(Insignia, pk=pk)
    if request.method == 'POST':
        form = InsigniaForm(request.POST, request.FILES, instance=insignia)
        if form.is_valid():
            form.save()
            messages.success(request, 'Insignia actualizada exitosamente.')
            return redirect('gestionar_insignias')
    else:
        form = InsigniaForm(instance=insignia)
    return render(request, 'entrenamiento/editar_insignia.html', {'form': form, 'insignia': insignia})

# Vista para eliminar una insignia
@staff_member_required
def eliminar_insignia(request, pk):
    insignia = get_object_or_404(Insignia, pk=pk)
    if request.method == 'POST':
        insignia.delete()
        messages.success(request, 'Insignia eliminada exitosamente.')
        return redirect('gestionar_insignias')
    return render(request, 'entrenamiento/eliminar_insignia.html', {'insignia': insignia})














# notificaciones 
from datetime import datetime, timedelta
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notificacion

@login_required
def notificaciones(request):
    # Obtener filtros de la solicitud GET
    filtro_estado = request.GET.get('estado', 'todas')
    filtro_fecha = request.GET.get('fecha', 'todas')

    # Obtener todas las notificaciones del usuario
    notificaciones = Notificacion.objects.filter(usuario=request.user)

    # Filtrar por estado
    if filtro_estado == 'no_leidas':
        notificaciones = notificaciones.filter(leido=False)
    elif filtro_estado == 'leidas':
        notificaciones = notificaciones.filter(leido=True)

    # Filtrar por fecha
    if filtro_fecha == 'hoy':
        inicio_hoy = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        notificaciones = notificaciones.filter(fecha_creacion__gte=inicio_hoy)
    elif filtro_fecha == 'semana':
        inicio_semana = datetime.now() - timedelta(days=7)
        notificaciones = notificaciones.filter(fecha_creacion__gte=inicio_semana)
    elif filtro_fecha == 'mes':
        inicio_mes = datetime.now() - timedelta(days=30)
        notificaciones = notificaciones.filter(fecha_creacion__gte=inicio_mes)

    # Paginación
    from django.core.paginator import Paginator
    paginator = Paginator(notificaciones.order_by('-fecha_creacion'), 10)  # 10 notificaciones por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Contexto para la plantilla
    context = {
        'notificaciones': page_obj,
        'page_obj': page_obj,
        'filtro_estado': filtro_estado,
        'filtro_fecha': filtro_fecha,
    }

    return render(request, 'main_app/notificaciones.html', context)

    



# Marcar como leídas las notificaciones
@login_required
def marcar_notificacion_como_leida(request, notificacion_id):
    # Obtener la notificación específica
    notificacion = get_object_or_404(Notificacion, id=notificacion_id, usuario=request.user)
    # Cambiar el estado de lectura a True
    notificacion.leido = True
    notificacion.save()
    # Redirigir a la página de notificaciones
    return redirect('notificaciones')



# para marca todas las notificaciones leidas
# views.py


@login_required
def marcar_todas_notificaciones_como_leidas(request):
    from .models import Notificacion  # Importación local para evitar la circularidad
    # Obtener todas las notificaciones no leídas del usuario
    Notificacion.objects.filter(usuario=request.user, leido=False).update(leido=True)
    # Redirigir a la página de notificaciones
    return HttpResponseRedirect(reverse('notificaciones'))




# Eliminar Notificaciones 
@login_required
def eliminar_notificacion(request, notificacion_id):
    notificacion = get_object_or_404(Notificacion, id=notificacion_id, usuario=request.user)
    notificacion.delete()
    return redirect('notificaciones')






# notificaciones/views.py o donde se crea la notificación


# Ejemplo de función para crear una notificación y enviarla por WebSocket
def crear_notificacion(usuario, mensaje):
    # Crear notificación en la base de datos
    notificacion = Notificacion.objects.create(usuario=usuario, mensaje=mensaje)

    # Enviar notificación en tiempo real
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'notificaciones_{usuario.id}',
        {'type': 'send_notification', 'message': mensaje}
    )



# para enviar una notificación a los clientes de parte de los administradores :

@user_passes_test(lambda u: u.is_staff)  # Solo permitido para administradores
def enviar_notificacion(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        mensaje = request.POST.get('mensaje')
        usuarios = User.objects.all()

        for usuario in usuarios:
            Notificacion.objects.create(titulo=titulo, mensaje=mensaje, usuario=usuario)
        
        messages.success(request, '¡Notificación enviada a todos los usuarios!')
        return redirect('enviar_notificacion')

    return render(request, 'main_app/enviar_notificacion.html')


# # una vista para que los usuarios puedan ver sus notificaciones 


@login_required
def lista_notificaciones(request):
    try:
        notificaciones = request.user.notificaciones.order_by('-fecha_creacion')
    except AttributeError:
        notificaciones = []  # Si no hay notificaciones, asigna una lista vacía.
    return render(request, 'main_app/lista_notificaciones.html', {
        'notificaciones': notificaciones
    })






def mi_vista(request):
    # Lógica de tu vista aquí
    if request.method == "POST":
        # Suponiendo que deseas enviar una notificación cuando se realiza un POST
        enviar_notificacion(request.user.id, "¡Tienes una nueva notificación!")
    
    return render(request, 'mi_template.html')


# views.py


def notificaciones_view(request):
    # Obtener todas las notificaciones del usuario
    notificaciones = Notificacion.objects.filter(user=request.user).order_by('-created_at')
    
    # Configurar paginación: 10 notificaciones por página
    paginator = Paginator(notificaciones, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'notificaciones.html', {'page_obj': page_obj})






# prueba para enviar notoficaciones 
from .utils import enviar_notificacion_en_tiempo_real
from django.http import HttpResponse

def enviar_notificacion_prueba(request):
    if request.user.is_authenticated:
        enviar_notificacion_en_tiempo_real(
            user=request.user,
            title="Nueva Notificación",
            message="¡Tienes una nueva notificación en tiempo real!"
        )
    return HttpResponse("Notificación enviada.")




# Vista para manejjar la subida de los video 

# views.py

def subir_video_leccion(request):
    if request.method == 'POST':
        form = VideoLeccionForm(request.POST, request.FILES)  # Asegúrate de usar request.FILES para archivos
        if form.is_valid():
            form.save()
            messages.success(request, '¡El video ha sido subido exitosamente!')
            return redirect('lista_entrenamiento')  # Redirige a la lista de lecciones
        else:
            messages.error(request, 'Hubo un error al subir el video. Por favor, revisa los campos.')
    else:
        form = VideoLeccionForm()
    
    
    
    return render(request, 'main_app/subir_video_leccion.html', {'form': form})



# secion para manejar el perfil del usuario 

# views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserProfileForm, UpdatePasswordForm, UpdateBackgroundForm

@login_required
def perfil_usuario(request):
    user = request.user
    
    # Formulario para actualizar información del perfil
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, instance=user)
        background_form = UpdateBackgroundForm(request.POST, request.FILES, instance=user.profile)
        password_form = UpdatePasswordForm(user=user, data=request.POST)
        
        if profile_form.is_valid() and background_form.is_valid():
            profile_form.save()
            background_form.save()
            messages.success(request, 'Tu perfil ha sido actualizado.')
            return redirect('perfil_usuario')
        
        if password_form.is_valid():
            user.set_password(password_form.cleaned_data['new_password1'])
            user.save()
            messages.success(request, 'Tu contraseña ha sido actualizada.')
            return redirect('perfil_usuario')
    else:
        profile_form = UserProfileForm(instance=user)
        background_form = UpdateBackgroundForm(instance=user.profile)
        password_form = UpdatePasswordForm(user=user)

    context = {
        'profile_form': profile_form,
        'background_form': background_form,
        'password_form': password_form,
    }
    return render(request, 'main_app/perfil_usuario.html', context)





# Seccion de plaanes 
# views.py
from django.shortcuts import render

def plan_basic(request):
    return render(request, 'planes/plan_basic.html')

def plan_professional(request):
    return render(request, 'planes/plan_professional.html')

def plan_enterprise(request):
    return render(request, 'planes/plan_enterprise.html')



# ----------------------------------------------------------------
# seccion de subsicripcion 
# En views.py

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def subscribe(request):
    if request.method == 'POST':
        # Aquí puedes manejar la lógica de registro y pago (esto es solo un ejemplo)
        # Suponiendo que ya has creado el modelo para gestionar suscripciones.
        # Puedes incluir un formulario de pago si usas algo como Stripe o PayPal.

        # Si la suscripción fue exitosa, redirige a una página de confirmación
        return redirect('subscription_success')
    
    return render(request, 'planes/subscribe.html')






# ----------------------------------------------------------------
# confirmacion de pago de suscripcion 

# En views.py
from django.shortcuts import render

def subscription_success(request):
    return render(request, 'planes/subscription_success.html')








#  ----------------------------------------------------------------
# views.py
from django.shortcuts import render, redirect
from .models import Testimonio
from .forms import TestimonioForm
from django.contrib.auth.decorators import login_required

def testimonios(request):
    testimonios = Testimonio.objects.filter(estado='aprobado').order_by('-fecha_creacion')
    return render(request, 'testimonios/testimonios_list.html', {'testimonios': testimonios})

@login_required
def agregar_testimonio(request):
    if request.method == 'POST':
        form = TestimonioForm(request.POST, request.FILES)
        if form.is_valid():
            testimonio = form.save(commit=False)
            testimonio.usuario = request.user
            testimonio.save()
            return redirect('testimonios')  # Redirige a la página de testimonios
    else:
        form = TestimonioForm()

    return render(request, 'testimonios/agregar_testimonio.html', {'form': form})



#  ----------------------------------------------------------------
# Testimonios de subscription 

# views.py
from .models import Testimonio

def mostrar_testimonios(request):
    testimonios = Testimonio.objects.filter(estado='aprobado').order_by('-fecha_creacion')
    return render(request, 'testimonios.html', {'testimonios': testimonios})







# ----------------------------------------------------------------

# Area para gestionar testimonios 
# ----------------------------------------------------------------
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def moderar_testimonios(request):
    testimonios = Testimonio.objects.all().order_by('-fecha_creacion')
    return render(request, 'testimonios/moderar_testimonios.html', {'testimonios': testimonios})

@staff_member_required
def cambiar_estado_testimonio(request, pk):
    testimonio = Testimonio.objects.get(pk=pk)
    if testimonio.estado == 'pendiente':
        testimonio.estado = 'aprobado'
    else:
        testimonio.estado = 'pendiente'
    testimonio.save()
    return redirect('moderar_testimonios')







# ----------------------------------------------------------------
# Centro de ayuda 

from django.shortcuts import render
from .models import FAQ, Categoria
from django.db.models import Q

# Vista para el centro de ayuda
def centro_ayuda(request):
    categorias = Categoria.objects.all()
    faqs = FAQ.objects.all()

    # Búsqueda de FAQs
    query = request.GET.get('q', '')
    if query:
        faqs = FAQ.objects.filter(
            Q(pregunta__icontains=query) | Q(respuesta__icontains=query)
        )
    
    return render(request, 'main_app/ayuda.html', {
        'categorias': categorias,
        'faqs': faqs,
        'query': query
    })
# ----------------------------------------------------------------
# Vista para Mostrar FAQs por Categoría 
from django.shortcuts import render, get_object_or_404
from .models import FAQ, Categoria

def preguntas_por_categoria(request, slug):
    # Obtener la categoría correspondiente al slug
    categoria = get_object_or_404(Categoria, slug=slug)
    # Filtrar las FAQs por la categoría
    faqs = FAQ.objects.filter(categoria=categoria)
    # Pasar los datos a la plantilla
    return render(request, 'main_app/preguntas_categoria.html', {
        'categoria': categoria,
        'faqs': faqs,
    })





# agrega una vista para gestionar el formulario. de preguntas frecuentes 

from django.shortcuts import render, redirect
from .forms import FAQForm
from django.contrib.auth.decorators import login_required

@staff_member_required
def agregar_faq(request):
    if request.method == 'POST':
        form = FAQForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ayuda')  # Redirige al centro de ayuda después de guardar
    else:
        form = FAQForm()
    return render(request, 'main_app/agregar_faq.html', {'form': form})





#  Crear vistas para listar y mostrar entradas
# views.py  Vista para Listar Publicaciones por Categoría
from django.shortcuts import render, get_object_or_404
from .models import BlogPost
from main_app import models

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.db.models import Q  # Importar Q para consultas avanzadas
from taggit.models import Tag # etiquetas 



from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def lista_blog(request, slug=None):
    """
    Vista para mostrar la lista de publicaciones del blog.
    Soporta filtros por categoría, búsqueda, etiquetas, y popularidad.
    Incluye paginación.
    """
    categorias = Categoria.objects.all()  # Todas las categorías
    query = request.GET.get('q', '')  # Término de búsqueda
    tag_slug = request.GET.get('tag', '')  # Slug de etiqueta
    popularidad = request.GET.get('popularidad', 'recientes')  # Orden por popularidad
    categoria = None
    tag = None

    # Filtrar publicaciones por categoría si se proporciona el slug
    if slug:
        categoria = get_object_or_404(Categoria, slug=slug)
        posts = BlogPost.objects.filter(categoria=categoria, publicado=True)
    else:
        posts = BlogPost.objects.filter(publicado=True)

    # Filtrar por búsqueda
    if query:
        posts = posts.filter(
            Q(titulo__icontains=query) | Q(contenido__icontains=query)
        )

    # Filtrar por etiquetas
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags=tag)

    # Ordenar publicaciones
    if popularidad == "vistas":
        posts = posts.order_by('-vistas')
    elif popularidad == "comentarios":
        posts = posts.annotate(num_comentarios=Count('comentarios')).order_by('-num_comentarios')
    else:  # Orden predeterminado: Más recientes
        posts = posts.order_by('-fecha_creacion')

    # Paginación
    paginator = Paginator(posts, 6)  # Mostrar 6 publicaciones por página
    page_number = request.GET.get('page', 1)
    try:
        page_posts = paginator.page(page_number)
    except PageNotAnInteger:
        page_posts = paginator.page(1)
    except EmptyPage:
        page_posts = paginator.page(paginator.num_pages)

    # Renderizar la plantilla con los datos
    return render(request, 'blog/lista_blog.html', {
        'page_posts': page_posts,  # Publicaciones en la página actual
        'categorias': categorias,  # Lista de categorías
        'slug': slug,  # Categoría activa
        'query': query,  # Búsqueda actual
        'tag': tag,  # Etiqueta activa
        'popularidad': popularidad,  # Filtro de popularidad activo
    })






from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count
from .models import BlogPost, Comentario
from .forms import ComentarioForm
from django.db.models import Count, Q

from bs4 import BeautifulSoup
import re

def detalle_blog(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)

    # Incrementar contador de vistas directamente
    post.vistas += 1
    post.save(update_fields=['vistas'])

    # Obtener comentarios principales y respuestas
    comentarios = post.comentarios.filter(aprobado=True, padre__isnull=True).order_by('-fecha_creacion').prefetch_related('respuestas')

    # Procesar el formulario de comentarios
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = ComentarioForm(request.POST)
            if form.is_valid():
                comentario = form.save(commit=False)
                comentario.post = post
                comentario.autor = request.user

                # Manejar respuestas a comentarios
                parent_id = request.POST.get('parent_id')
                if parent_id:
                    try:
                        comentario.padre = Comentario.objects.get(id=parent_id, post=post)
                    except Comentario.DoesNotExist:
                        comentario.padre = None  # Ignorar si no existe el padre

                comentario.save()
                return redirect('detalle_blog', slug=post.slug)
        else:
            return redirect('login')
    else:
        form = ComentarioForm()

    # Publicaciones relacionadas
    related_posts = BlogPost.objects.filter(
        Q(categoria=post.categoria) | Q(tags__in=post.tags.all()),
        publicado=True
    ).exclude(id=post.id).distinct().annotate(shared_tags=Count('tags')).order_by('-shared_tags', '-fecha_creacion')[:5]

    # Publicaciones más vistas
    mas_vistas = BlogPost.objects.filter(publicado=True).order_by('-vistas')[:5]

    # Índice interactivo basado en encabezados del contenido
    encabezados = []
    contenido_html = post.contenido
    if contenido_html:
        soup = BeautifulSoup(contenido_html, 'html.parser')
        for header in soup.find_all(['h2', 'h3']):
            header_id = re.sub(r'\s+', '-', header.get_text(strip=True).lower())
            header['id'] = header_id
            encabezados.append({'nivel': header.name, 'texto': header.get_text(strip=True), 'id': header_id})
        post.contenido = str(soup)  # Actualizar contenido con IDs

    return render(request, 'blog/detalle_blog.html', {
        'post': post,
        'comentarios': comentarios,
        'form': form,
        'related_posts': related_posts,
        'mas_vistas': mas_vistas,
        'encabezados': encabezados,
    })







@login_required
def votar_comentario(request, comentario_id, voto):
    """
    Vista para manejar los votos de comentarios.
    """
    comentario = get_object_or_404(Comentario, id=comentario_id)
    if voto == 'positivo':
        comentario.voto_positivo += 1
    elif voto == 'negativo':
        comentario.voto_negativo += 1
    comentario.save()
    return JsonResponse({'voto_positivo': comentario.voto_positivo, 'voto_negativo': comentario.voto_negativo})



# OPCION PARA RESPONDER AL COMENTARIO
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

@login_required
def responder_comentario(request, comentario_id):
    """
    Vista para responder a un comentario.
    Permite a los usuarios autenticados responder a comentarios existentes.
    """
    comentario_padre = get_object_or_404(Comentario, id=comentario_id)
    
    # Solo se permite el método POST para crear respuestas
    if request.method == 'POST':
        contenido = request.POST.get('contenido')
        if contenido:
            nueva_respuesta = Comentario.objects.create(
                post=comentario_padre.post,  # Relacionar con el mismo post que el comentario padre
                autor=request.user,         # El autor de la respuesta es el usuario autenticado
                contenido=contenido,        # Contenido de la respuesta
                padre=comentario_padre      # Relacionar como hijo del comentario padre
            )
            
            # Verifica si la solicitud es AJAX (para respuestas dinámicas)
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'mensaje': 'Respuesta creada exitosamente',
                    'autor': nueva_respuesta.autor.username,
                    'contenido': nueva_respuesta.contenido,
                    'fecha_creacion': nueva_respuesta.fecha_creacion.strftime('%d %b %Y %H:%M')
                })

    # Redirigir al detalle del blog si no es una solicitud AJAX
    return redirect('detalle_blog', slug=comentario_padre.post.slug)




    
# comentarios del blog 
# views.py
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Comentario, BlogPost

def agregar_comentario(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(BlogPost, id=post_id)
        comentario_contenido = request.POST['contenido']
        
        # Crear el comentario
        comentario = Comentario.objects.create(
            post=post,
            autor=request.user,
            contenido=comentario_contenido,
            aprobado=False  # Se aprueba manualmente en el panel de administración
        )
        comentario.save()

        # Redirigir al detalle de la publicación
        return HttpResponseRedirect(reverse('blog_detail', args=[post.id]))




# Vista para gestionar suscripciones 

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SuscripcionForm

def suscribirse(request):
    if request.method == 'POST':
        form = SuscripcionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Te has suscrito exitosamente!")
        else:
            messages.error(request, "Este correo ya está registrado.")
    else:
        form = SuscripcionForm()
    return render(request, 'blog/suscripcion.html', {'form': form})



# Vista para manejar reacciones 

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import BlogPost, Reaccion

@login_required
def reaccionar(request, post_id, tipo):
    """
    Maneja las reacciones (like/love) de un usuario en una publicación.
    """
    if request.method == 'POST':
        post = get_object_or_404(BlogPost, id=post_id)

        # Verifica que el tipo de reacción sea válido
        if tipo not in ['like', 'love']:
            return JsonResponse({'error': 'Tipo de reacción no válido'}, status=400)

        # Intenta obtener una reacción existente
        reaccion, creada = Reaccion.objects.get_or_create(usuario=request.user, post=post)

        if not creada:
            if reaccion.tipo == tipo:
                # Si el tipo es el mismo, elimina la reacción
                reaccion.delete()
                likes_count = post.reacciones.filter(tipo='like').count()
                loves_count = post.reacciones.filter(tipo='love').count()
                return JsonResponse({
                    'status': 'removed',
                    'likes_count': likes_count,
                    'loves_count': loves_count,
                })
            else:
                # Si el tipo es diferente, actualiza la reacción
                reaccion.tipo = tipo
                reaccion.save()
        else:
            # Si no existía, crea una nueva reacción
            reaccion.tipo = tipo
            reaccion.save()

        # Recalcula los contadores
        likes_count = post.reacciones.filter(tipo='like').count()
        loves_count = post.reacciones.filter(tipo='love').count()

        return JsonResponse({
            'status': 'updated' if not creada else 'created',
            'likes_count': likes_count,
            'loves_count': loves_count,
        })

    return JsonResponse({'error': 'Método no permitido'}, status=405)




# Agrega una vista para manejar la página de contacto y, opcionalmente, el envío de formularios.


from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from .forms import ContactForm

def contacto(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Extraer datos del formulario
            nombre = form.cleaned_data['nombre']
            email = form.cleaned_data['email']
            mensaje = form.cleaned_data['mensaje']

            # Enviar correo
            try:
                send_mail(
                    f"Consulta de {nombre} ({email})",
                    mensaje,
                    email,  # Remitente
                    ['tu_correo@tu_dominio.com'],  # Destinatario
                )
                messages.success(request, 'Tu mensaje ha sido enviado exitosamente.')
                return redirect('contacto')
            except Exception as e:
                messages.error(request, 'Ocurrió un error al enviar tu mensaje. Inténtalo más tarde.')
    else:
        form = ContactForm()

    return render(request, 'main_app/contacto.html', {'form': form})
