import os
from .forms import RegistroForm, EditarPerfilForm, MiFormularioCambioContrasena
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.cache import never_cache
from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.views import View
from django.contrib.auth.views import PasswordResetView
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.http import JsonResponse
from .models import Asistencia, Notificacion, Clase
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
from django.utils.dateparse import parse_date
from django.core.serializers import serialize
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from django.utils.timezone import now
from django.utils.timezone import localtime
from .models import Asistencia, Notificacion
from .forms import JustificativoForm
from ontime_app.models import Asistencia

# --- Vistas de Autenticación y Perfil ---

def iniciar_sesion(request):
    """
    Vista para manejar el inicio de sesión de usuarios.
    Autentica al usuario y redirige según su rol.
    """
    correo = None

    if request.method == 'POST':
        username = request.POST.get('correo')
        contrasena = request.POST.get('contrasena')

        # Autentica al usuario con las credenciales
        user = authenticate(request, username=username, password=contrasena)

        if user is not None:
            # Inicia sesión y redirige según el rol
            login(request, user)
            rol = user.rol

            if rol == 'aprendiz':
                return redirect('inicio_aprendiz')
            elif rol == 'instructor':
                return redirect('inicio_instructor')
            elif rol == 'admin':
                return redirect('inicio_admin')
            else:
                # Manejo de rol desconocido
                messages.error(request, 'Rol desconocido, contacta al admin.')
                logout(request)
                return redirect('iniciar_sesion')
        else:
            # Muestra mensaje de error si las credenciales son incorrectas
            messages.error(request, 'Correo o contraseña incorrectos.')
            correo = request.POST.get('correo')
            return render(request, 'ontime_app/iniciar_sesion.html', {'correo': correo})

    return render(request, 'ontime_app/iniciar_sesion.html', {'correo': correo})

def registrarse(request): 
    """
    Vista para el registro de nuevos usuarios.
    Crea un nuevo usuario si el formulario es válido.
    """
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            # Guarda el nuevo usuario
            form.save()
            messages.success(request, 'Cuenta creada correctamente.')
            return redirect('iniciar_sesion')
        else:
            # Muestra errores del formulario
            print(form.errors)
            messages.error(request, 'Corrige los errores del formulario.')
    else:
        form = RegistroForm()
    
    return render(request, 'ontime_app/registrarse.html', {'form': form})

@never_cache
def cerrar_sesion(request):
    """
    Vista para cerrar la sesión del usuario actual.
    """
    logout(request)
    return redirect('inicio')

@never_cache
@login_required
def eliminar_foto_perfil(request):
    """
    Vista para eliminar la foto de perfil del usuario logueado.
    Elimina el archivo físico y la referencia en la base de datos.
    """
    usuario = request.user

    if usuario.foto_perfil:
        # Elimina la foto de perfil del sistema de archivos
        ruta = os.path.join(settings.MEDIA_ROOT, str(usuario.foto_perfil))
        if os.path.isfile(ruta):
            os.remove(ruta)
        # Elimina la referencia en la base de datos
        usuario.foto_perfil = None
        usuario.save()

    return redirect('editar_perfil')

# --- Vistas de Edición de Perfil ---

@never_cache
@login_required(login_url='iniciar_sesion')
def editar_perfil(request):
    usuario = request.user
    rol = usuario.rol

    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            nueva_contra = form.cleaned_data.get('password')
            if nueva_contra:
                usuario.set_password(nueva_contra)
            form.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            if rol == 'aprendiz':
                return redirect('inicio_aprendiz')
            elif rol == 'instructor':
                return redirect('inicio_instructor')
            else:
                return redirect('inicio')
    else:
        form = EditarPerfilForm(instance=usuario)

    return render(request, 'ontime_app/editar_perfil.html', {
        'form': form,
        'usuario': usuario,
        'rol': rol,
    })

# --- Vista para Editar Perfil Único ---

@never_cache
@login_required(login_url='iniciar_sesion')
def editar_perfil_unico(request):
    usuario = request.user

    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            user = form.save(commit=False)

            # Si se quiere cambiar la contraseña
            nueva_contraseña = form.cleaned_data.get('password')
            if nueva_contraseña:
                user.set_password(nueva_contraseña)

            user.save()

            messages.success(request, '¡Perfil actualizado correctamente!')

            # Redirige según el rol
            if usuario.rol == 'aprendiz':
                return redirect('inicio_aprendiz')
            elif usuario.rol == 'instructor':
                return redirect('inicio_instructor')
            elif usuario.rol == 'admin':
                return redirect('inicio_admin')
            else:
                return redirect('inicio')
    else:
        form = EditarPerfilForm(instance=usuario)

    return render(request, 'ontime_app/editar_perfil.html', {
        'form': form,
        'usuario': usuario,
        'rol': usuario.rol
    })

# --- Vistas de Recuperación y Cambio de Contraseña ---

def recuperar_contraseña(request):
    """
    Vista para solicitar el restablecimiento de contraseña.
    Envía un correo con un enlace de recuperación.
    """
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            # Envía el correo de restablecimiento de contraseña
            form.save(
                request=request,
                email_template_name='registration/password_reset_email.html',
                subject_template_name='registration/password_reset_subject.txt',
                use_https=request.is_secure()
            )
            messages.success(request, 'Se ha enviado un enlace de recuperación a tu correo.')
            return redirect('recuperar_contraseña')
    else:
        form = PasswordResetForm()
    return render(request, 'ontime_app/recuperar_contraseña.html', {'form': form})

class MiPasswordResetConfirmView(View):
    """
    Vista para confirmar el restablecimiento de contraseña y permitir al usuario cambiarla.
    """
    template_name = 'recuperar_contraseña_confirm.html'  # Plantilla para cambiar la contraseña

    def get_user(self, uidb64):
        """Decodifica el UID y obtiene el usuario."""
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        return user

    def get(self, request, uidb64=None, token=None):
        """Renderiza el formulario para cambiar la contraseña."""
        user = self.get_user(uidb64)
        if user is not None and default_token_generator.check_token(user, token):
            form = MiFormularioCambioContrasena(user=user)
            return render(request, self.template_name, {'form': form})
        else:
            return render(request, 'password_reset_invalid.html')  # Plantilla para token inválido

    def post(self, request, uidb64=None, token=None):
        """Procesa el cambio de contraseña."""
        user = self.get_user(uidb64)
        if user is not None and default_token_generator.check_token(user, token):
            form = MiFormularioCambioContrasena(user=user, data=request.POST)
            if form.is_valid():
                form.save()
                return redirect('contraseña_actualizada')  # Redirige a pantalla de confirmación
            else:
                return render(request, self.template_name, {'form': form})
        else:
            return render(request, 'password_reset_invalid.html')

class CustomPasswordResetView(PasswordResetView):
    """
    Vista personalizada para el envío de correo de recuperación.
    Permite enviar correos con versiones HTML y de texto plano.
    """
    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        """Envía el correo de restablecimiento."""
        subject = render_to_string(subject_template_name, context).strip()
        body = render_to_string(email_template_name, context)
        html_body = render_to_string(html_email_template_name or email_template_name, context)

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        email_message.attach_alternative(html_body, 'text/html')
        email_message.send()

def cambiar_contrasena(request, uidb64, token):
    """
    Vista para cambiar la contraseña usando un token de recuperación.
    """
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        usuario = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        usuario = None

    if usuario is not None and default_token_generator.check_token(usuario, token):
        if request.method == "POST":
            form = MiFormularioCambioContrasena(user=usuario, data=request.POST)
            if form.is_valid():
                form.save()
                return redirect('contraseña_actualizada')
        else:
            form = MiFormularioCambioContrasena(user=usuario)

        return render(request, 'ontime_app/password_reset_confirm.html', {'form': form})
    else:
        return render(request, 'ontime_app/password_reset_invalid.html')

def cambiar_contraseña(request):
    """
    Vista para mostrar el formulario de cambio de contraseña.
    """
    return render(request, 'ontime_app/cambiar_contraseña.html')

def contraseña_actualizada(request):
    """
    Vista para mostrar un mensaje de confirmación de contraseña actualizada.
    """
    return render(request, 'ontime_app/contraseña_actualizada.html')

# --- Vistas por Rol: Aprendiz ---

@never_cache
@login_required(login_url='iniciar_sesion')
def inicio_aprendiz(request):
    """
    Página de inicio para usuarios con rol 'aprendiz'.
    Requiere autenticación y redirige si el rol no coincide.
    """
    if request.user.rol != 'aprendiz':
        return redirect('inicio')
    usuario = request.user
    return render(request, 'ontime_app/inicio_aprendiz.html', {'usuario': usuario})

@never_cache
@login_required(login_url='iniciar_sesion')
def registrar_asistencia(request):
    """
    Vista para que el aprendiz registre su asistencia.
    """
    if request.user.rol != 'aprendiz':
        return redirect('inicio')
    return render(request, 'ontime_app/registrar_asistencia.html')

@login_required
def notificaciones_1(request):
    """
    Vista para mostrar las notificaciones de un aprendiz, con paginación.
    """
    if request.user.rol != 'aprendiz':
        return redirect('inicio')

    usuario = request.user
    # Obtiene las notificaciones del usuario, ordenadas por fecha
    notis = Notificacion.objects.filter(usuario=usuario).order_by('-fecha')
    paginador = Paginator(notis, 5)  # 5 notificaciones por página
    try:
        primera_pagina = paginador.page(1)
    except EmptyPage:
        primera_pagina = []

    return render(request, 'ontime_app/notificaciones_1.html', {
        'notificaciones': primera_pagina,
        'hay_mas': primera_pagina.has_next() if primera_pagina else False
    })

@never_cache
@login_required(login_url='iniciar_sesion')
def historial_1(request):
    """
    Vista del historial para usuarios con rol 'aprendiz'.
    """
    if request.user.rol != 'aprendiz':
        return redirect('inicio')
    return render(request, 'ontime_app/historial_1.html')

@never_cache
@login_required(login_url='iniciar_sesion')
def justificativos_1(request):
    """
    Vista de justificativos para usuarios con rol 'aprendiz'.
    """
    if request.user.rol != 'aprendiz':
        return redirect('inicio')
    return render(request, 'ontime_app/justificativos_1.html')

# --- Vistas por Rol: Instructor ---

@never_cache
@login_required(login_url='iniciar_sesion')
def inicio_instructor(request):
    """
    Página de inicio para usuarios con rol 'instructor'.
    Requiere autenticación y redirige si el rol no coincide.
    """
    if request.user.rol != 'instructor':
        return redirect('inicio')
    return render(request, 'ontime_app/inicio_instructor.html')

@never_cache
@login_required(login_url='iniciar_sesion')
def generar_qr(request):
    """
    Vista para que el instructor genere códigos QR.
    """
    if request.user.rol != 'instructor':
        return redirect('inicio')
    return render(request, 'ontime_app/generar_qr.html')

@never_cache
@login_required(login_url='iniciar_sesion')
def consultar_asistencias(request):
    """
    Vista para que el instructor consulte asistencias.
    """
    if request.user.rol != 'instructor':
        return redirect('inicio')
    return render(request, 'ontime_app/consultar_asistencias.html')

@never_cache
@login_required(login_url='iniciar_sesion')
def alertas(request):
    """
    Vista para que el instructor gestione alertas.
    """
    if request.user.rol != 'instructor':
        return redirect('inicio')
    return render(request, 'ontime_app/alertas.html')

@never_cache
@login_required(login_url='iniciar_sesion')
def gestion_reportes(request):
    """
    Vista para que el instructor gestione reportes.
    """
    if request.user.rol != 'instructor':
        return redirect('inicio')
    return render(request, 'ontime_app/gestion_reportes.html')

# --- Vistas Generales ---

def inicio(request):
    """
    Página de inicio general para usuarios no autenticados.
    """
    return render(request, 'ontime_app/inicio.html')

def contacto(request):
    """
    Vista para la página de contacto.
    """
    return render(request, 'ontime_app/contacto.html')

def ayuda(request):
    """
    Vista para la página de ayuda.
    """
    return render(request, 'ontime_app/ayuda.html')

def acerca_de(request):
    """
    Vista para la página "Acerca de".
    """
    return render(request, 'ontime_app/acerca_de.html')

# --- Vistas de Documentación y Diseño ---

def modelo_relacional(request):
    """Vista para mostrar el modelo relacional."""
    return render(request, 'ontime_app/modelo_relacional.html')

def normalizacion_mr(request):
    """Vista para mostrar la normalización del modelo relacional."""
    return render(request, 'ontime_app/normalizacion_mr.html')

def diccionario_datos(request):
    """Vista para mostrar el diccionario de datos (primera versión)."""
    return render(request, 'ontime_app/diccionario_datos.html')

def diccionario_datoss(request):
    """Vista para mostrar el diccionario de datos (segunda versión)."""
    return render(request, 'ontime_app/diccionario_datoss.html')

def sentencias(request):
    """Vista para mostrar sentencias SQL o similares."""
    return render(request, 'ontime_app/sentencias.html')

def diagrama_clases(request):
    """Vista para mostrar el diagrama de clases."""
    return render(request, 'ontime_app/diagrama_clases.html')

# --- Vistas por Rol: Administrador ---

def es_admin(user):
    """
    Función de ayuda para verificar si un usuario es administrador.
    """
    return user.is_authenticated and user.rol == 'admin'

@login_required(login_url='iniciar_sesion')
@user_passes_test(es_admin, login_url='iniciar_sesion')
def inicio_admin(request):
    """
    Página de inicio para usuarios con rol 'admin'.
    Permite el registro de nuevos usuarios desde esta vista.
    """
    form = RegistroForm()

    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Usuario creado correctamente!')
            return redirect('inicio_admin')

    return render(request, 'ontime_app/inicio_admin.html', {'form': form})

@never_cache
@login_required(login_url='iniciar_sesion')
def gestion_usuarios(request):
    """
    Vista para que el administrador gestione usuarios.
    """
    if request.user.rol != 'admin':
        return redirect('inicio')
    return render(request, 'ontime_app/gestion_usuarios.html')

@never_cache
@login_required(login_url='iniciar_sesion')
def ver_asistencias(request):
    """
    Vista para que el administrador vea las asistencias.
    """
    if request.user.rol != 'admin':
        return redirect('inicio')
    return render(request, 'ontime_app/ver_asistencias.html')

@never_cache
@login_required(login_url='iniciar_sesion')
def gestion_alertas(request):
    """
    Vista para que el administrador gestione alertas.
    """
    if request.user.rol != 'admin':
        return redirect('inicio')
    return render(request, 'ontime_app/gestion_alertas.html')

@never_cache
@login_required(login_url='iniciar_sesion')
def reportes(request):
    """
    Vista para que el administrador genere reportes.
    """
    if request.user.rol != 'admin':
        return redirect('inicio')
    return render(request, 'ontime_app/reportes.html')

@never_cache
@login_required(login_url='iniciar_sesion')
def gestion_horarios(request):
    """
    Vista para que el administrador gestione horarios.
    """
    if request.user.rol != 'admin':
        return redirect('inicio')
    return render(request, 'ontime_app/gestion_horarios.html')

@never_cache
@login_required(login_url='iniciar_sesion')
def control_asistencia(request):
    """
    Vista para que el administrador controle la asistencia.
    """
    if request.user.rol != 'admin':
        return redirect('inicio')
    return render(request, 'ontime_app/control_asistencia.html')

@never_cache
@login_required(login_url='iniciar_sesion')
def carga_masiva(request):
    """
    Vista para que el administrador realice cargas masivas de datos.
    """
    if request.user.rol != 'admin':
        return redirect('inicio')
    return render(request, 'ontime_app/carga_masiva.html')

@never_cache
@login_required(login_url='iniciar_sesion')
def historial(request):
    """
    Vista del historial para usuarios con rol 'admin'.
    """
    if request.user.rol != 'admin':
        return redirect('inicio')
    return render(request, 'ontime_app/historial.html')

@login_required
@user_passes_test(es_admin)
def crear_usuario(request):
    """
    Vista para que el administrador cree nuevos usuarios.
    """
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario creado con éxito.")
            return redirect('nombre_de_la_ruta_a_donde_quieras_llevar_al_usuario')
        else:
            messages.error(request, "Algo está mal con los datos, revisa bien.")
    else:
        form = RegistroForm()
    
    return render(request, 'ontime_app/crear_usuario.html', {'form': form})

# --- Vistas para el registro de asistencia (AJAX) ---

@login_required
def registrar_asistencia(request):
    if request.method == 'POST':
        user = request.user
        codigo = request.POST.get('codigo')

        if not codigo:
            return JsonResponse({'status': 'fail', 'msg': 'Código es obligatorio'})

        ahora = localtime()

        inicio_dia = ahora.replace(hour=0, minute=0, second=0, microsecond=0)
        fin_dia = ahora.replace(hour=23, minute=59, second=59, microsecond=999999)

        existe = Asistencia.objects.filter(
            aprendiz=user,
            fecha__range=(inicio_dia, fin_dia)
        ).exists()

        if existe:
            return JsonResponse({'status': 'fail', 'msg': 'Ya registraste asistencia hoy.'})
        
        # Crear nueva asistencia
        nueva_asistencia = Asistencia.objects.create(
            aprendiz=user,
            codigo=codigo,
            fecha=ahora,
            validada=True
        )

    # Crear notificación para avisar
        Notificacion.objects.create(
            usuario=user,
            titulo="Registro de Asistencia",
            descripcion=f"Has registrado tu asistencia correctamente el {ahora.strftime('%d/%m/%Y a las %H:%M')}",
            tipo="asistencia"
        )

        return JsonResponse({'status': 'ok', 'msg': 'Asistencia registrada.'})

    # Si es GET, mostramos el template para escanear o ingresar código
    return render(request, 'ontime_app/registrar_asistencia.html')

# --- Vistas para Notificaciones ---

@login_required
def notificaciones(request):
    """
    Vista para mostrar todas las notificaciones del usuario actual.
    """
    notificaciones = Notificacion.objects.filter(usuario=request.user).order_by('-fecha')
    return render(request, 'ontime_app/notificaciones.html', {'notificaciones': notificaciones})

@require_POST
def marcar_notificacion_leida(request, id):
    """
    Marca una notificación específica como leída.
    Solo accesible vía POST.
    """
    notificacion = get_object_or_404(Notificacion, id=id, usuario=request.user)
    notificacion.leida = True
    notificacion.save()
    return JsonResponse({'status': 'ok', 'id': id})

@require_POST
def eliminar_notificacion(request, id):
    """
    Elimina una notificación específica.
    Solo accesible vía POST.
    """
    notificacion = get_object_or_404(Notificacion, id=id, usuario=request.user)
    notificacion.delete()
    return JsonResponse({'status': 'ok', 'id': id})

@login_required
def filtrar_notificaciones(request):
    """
    Filtra las notificaciones del usuario según tipo y fecha.
    Retorna HTML parcial con las notificaciones filtradas.
    """
    tipo = request.GET.get('tipo')
    fecha = request.GET.get('fecha')

    notificaciones = Notificacion.objects.filter(usuario=request.user)

    if tipo:
        notificaciones = notificaciones.filter(tipo=tipo)
    if fecha:
        notificaciones = notificaciones.filter(fecha__date=fecha)

    html = render_to_string('ontime_app/partials/partial_notificaciones.html', {'notificaciones': notificaciones})
    return JsonResponse({'html': html})

def cargar_mas_notificaciones(request):
    """
    Carga más notificaciones para la paginación infinita.
    """
    pagina = request.GET.get('pagina', 1)
    tipo = request.GET.get('tipo')
    fecha = request.GET.get('fecha')

    notis = Notificacion.objects.filter(usuario=request.user).order_by('-fecha')

    if tipo:
        notis = notis.filter(tipo=tipo)
    if fecha:
        notis = notis.filter(fecha__date=fecha)

    paginator = Paginator(notis, 10) # 10 notificaciones por página

    try:
        notis_pagina = paginator.page(pagina)
    except (EmptyPage, PageNotAnInteger):
        return JsonResponse({'html': '', 'hay_mas': False})

    html = render_to_string('ontime_app/partials/partial_notificaciones.html', {'notificaciones': notis_pagina})
    hay_mas = notis_pagina.has_next()

    return JsonResponse({'html': html, 'hay_mas': hay_mas})


def historial_api(request):
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    queryset = Asistencia.objects.all().order_by('-fecha')

    if fecha_inicio and fecha_fin:
        queryset = queryset.filter(fecha__date__range=[fecha_inicio, fecha_fin])

    datos = []
    for asistencia in queryset:
        datos.append({
            'id': asistencia.id,
            'fecha': asistencia.fecha.strftime('%Y-%m-%d'),
            'curso': asistencia.codigo,  # Aquí usamos 'codigo' como el nombre de la clase o módulo
            'estado': 'Asistido' if asistencia.validada else 'Faltante',
            'detalles': f"Asistencia de {asistencia.aprendiz.username}. Estado: {'Validada' if asistencia.validada else 'No validada'}."
        })

    return JsonResponse(datos, safe=False)


@login_required
def historial_asistencia(request):
    return render(request, 'ontime_app/historial_1.html')

@login_required
def cargar_mas_historial(request):
    try:
        pagina = int(request.GET.get('pagina', 1))
        fecha_inicio = request.GET.get('fecha_inicio')
        fecha_fin = request.GET.get('fecha_fin')

        historial = Asistencia.objects.filter(aprendiz=request.user).order_by('-fecha')

        if fecha_inicio:
            historial = historial.filter(fecha__gte=fecha_inicio)
        if fecha_fin:
            historial = historial.filter(fecha__lte=fecha_fin)

        paginator = Paginator(historial, 5)
        page_obj = paginator.get_page(pagina)

        if not page_obj.object_list.exists():
            return JsonResponse({'html': '', 'hay_mas': False, 'vacio': True})

        html = render_to_string('ontime_app/partials/_asistencia_item.html', {'historial': page_obj})
        return JsonResponse({'html': html, 'hay_mas': page_obj.has_next(), 'vacio': False})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def filtrar_asistencia(request):
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    query = Asistencia.objects.filter(aprendiz=request.user)

    if fecha_inicio:
        query = query.filter(fecha__gte=parse_date(fecha_inicio))
    if fecha_fin:
        query = query.filter(fecha__lte=parse_date(fecha_fin))

    datos = []
    for a in query.order_by('-fecha'):
        datos.append({
            'id': a.id,
            'fecha': a.fecha.strftime('%Y-%m-%d %H:%M'),
            'curso': 'Programación de software',
            'estado': 'Asistido' if a.validada else 'No asistió',
            'detalles': f'Código: {a.codigo}, validado: {a.validada}'
        })

    return JsonResponse({'datos': datos})


@login_required
def subir_justificativo(request):
    if request.method == 'POST':
        form = JustificativoForm(request.POST, request.FILES)
        if form.is_valid():
            justificativo = form.save(commit=False)
            justificativo.usuario = request.user
            justificativo.save()
            return render(request, 'ontime_app/subir_justificativo.html', {
                'form': JustificativoForm(),  # formulario limpio
                'mensaje_exito': True,
            })
    else:
        form = JustificativoForm()

    print("DEBUG FORM:", form)
    print("DEBUG FIELDS:", dir(form))

    return render(request, 'ontime_app/subir_justificativo.html', {
        'form': form
    })


@login_required
def progreso_asistencia(request):
    user = request.user

    total_clases = Clase.objects.count()
    asistencias = Asistencia.objects.filter(aprendiz=user).count()

    if total_clases > 0:
        porcentaje = round((asistencias / total_clases) * 100)
    else:
        porcentaje = 0

    return JsonResponse({'porcentaje': porcentaje})
