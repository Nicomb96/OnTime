import os
from .forms import RegistroForm, EditarPerfilForm, MiFormularioCambioContrasena
from django.shortcuts import render, redirect
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
from .models import Asistencia
from django.utils import timezone

# Vista para iniciar sesión
def iniciar_sesion(request):
    correo = None

    if request.method == 'POST':
        username = request.POST.get('correo')
        contrasena = request.POST.get('contrasena')

        user = authenticate(request, username=username, password=contrasena)

        if user is not None:
            login(request, user)
            rol = user.rol

            if rol == 'aprendiz':
                return redirect('inicio_aprendiz')
            elif rol == 'instructor':
                return redirect('inicio_instructor')
            elif rol == 'admin':
                return redirect('inicio_admin')
            else:
                # En caso de que alguien tenga un rol que no exista
                messages.error(request, 'Rol desconocido, contacta al admin.')
                logout(request)
                return redirect('iniciar_sesion')
        else:
            messages.error(request, 'Correo o contraseña incorrectos.')
            correo = request.POST.get('correo')
            return render(request, 'ontime_app/iniciar_sesion.html', {'correo': correo})

    return render(request, 'ontime_app/iniciar_sesion.html', {'correo': correo})

# Vista para registrarse
def registrarse(request): 
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cuenta creada correctamente.')
            return redirect('iniciar_sesion')
        else:
            print(form.errors)
            messages.error(request, 'Corrige los errores del formulario.')
    else:
        form = RegistroForm()
    
    return render(request, 'ontime_app/registrarse.html', {'form': form})

# Vista para cerrar sesión
@never_cache
def cerrar_sesion(request):
    logout(request)
    return redirect('inicio')

# Vista para eliminar foto de perfil
@never_cache
@login_required
def eliminar_foto_perfil(request):
    usuario = request.user

    if usuario.foto_perfil:
        ruta = os.path.join(settings.MEDIA_ROOT, str(usuario.foto_perfil))
        if os.path.isfile(ruta):
            os.remove(ruta)
        usuario.foto_perfil = None
        usuario.save()

    return redirect('editar_perfil_2')

# Vista para recuperar la contraseña
def recuperar_contraseña(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
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

# Vista para mostrar mensaje de contraseña actualizada
class MiPasswordResetConfirmView(View):
    template_name = 'recuperar_contraseña_confirm.html'  # Plantilla para cambiar la contraseña

    def get_user(self, uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        return user

    def get(self, request, uidb64=None, token=None):
        user = self.get_user(uidb64)
        if user is not None and default_token_generator.check_token(user, token):
            form = MiFormularioCambioContrasena(user=user)
            return render(request, self.template_name, {'form': form})
        else:
            return render(request, 'password_reset_invalid.html')  # Plantilla para token inválido

    def post(self, request, uidb64=None, token=None):
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

# Vista personalizada para el envío del correo de recuperación
class CustomPasswordResetView(PasswordResetView):
    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):

        # Renderizar asunto del correo
        subject = render_to_string(subject_template_name, context).strip()

        # Renderizar cuerpo en texto plano
        body = render_to_string(email_template_name, context)

        # Renderizar cuerpo en HTML
        html_body = render_to_string(html_email_template_name or email_template_name, context)

        # Construir y enviar correo con versión HTML y texto plano
        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        email_message.attach_alternative(html_body, 'text/html')
        email_message.send()

# Vista para cambiar contraseña con token (confirmación)
def cambiar_contrasena(request, uidb64, token):
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

# Vista para mostrar formulario para cambiar la contraseña
def cambiar_contraseña(request):
    return render(request, 'ontime_app/cambiar_contraseña.html')

# Vista para mostrar mensaje de contraseña actualizada
def contraseña_actualizada(request):
    return render(request, 'ontime_app/contraseña_actualizada.html')

# Vistas para la página de inicio según rol

# Inicio aprendiz
@never_cache
@login_required(login_url='iniciar_sesion')
def inicio_aprendiz(request):
    if request.user.rol != 'aprendiz':
        return redirect('inicio')
    usuario = request.user
    return render(request, 'ontime_app/inicio_aprendiz.html', {'usuario': usuario})

# Registrar asistencia (aprendiz)
@never_cache
@login_required(login_url='iniciar_sesion')
def registrar_asistencia(request):
    if request.user.rol != 'aprendiz':
        return redirect('inicio')
    return render(request, 'ontime_app/registrar_asistencia.html')

# Notificaciones (aprendiz)
@never_cache
@login_required(login_url='iniciar_sesion')
def notificaciones_1(request):
    if request.user.rol != 'aprendiz':
        return redirect('inicio')
    return render(request, 'ontime_app/notificaciones_1.html')

# Historial (aprendiz)
@never_cache
@login_required(login_url='iniciar_sesion')
def historial_1(request):
    if request.user.rol != 'aprendiz':
        return redirect('inicio')
    return render(request, 'ontime_app/historial_1.html')

# Justificativos (aprendiz)
@never_cache
@login_required(login_url='iniciar_sesion')
def justificativos_1(request):
    if request.user.rol != 'aprendiz':
        return redirect('inicio')
    return render(request, 'ontime_app/justificativos_1.html')

# Editar perfil 1 (aprendiz)
@never_cache
@login_required(login_url='iniciar_sesion')
def editar_perfil_1(request):
    if request.user.rol != 'aprendiz':
        return redirect('inicio')
    return render(request, 'ontime_app/editar_perfil_1.html')

# Inicio instructor
@never_cache
@login_required(login_url='iniciar_sesion')
def inicio_instructor(request):
    if request.user.rol != 'instructor':
        return redirect('inicio')
    return render(request, 'ontime_app/inicio_instructor.html')

# Generar QR (instructor)
@never_cache
@login_required(login_url='iniciar_sesion')
def generar_qr(request):
    if request.user.rol != 'instructor':
        return redirect('inicio')
    return render(request, 'ontime_app/generar_qr.html')

# Consultar asistencias (instructor)
@never_cache
@login_required(login_url='iniciar_sesion')
def consultar_asistencias(request):
    if request.user.rol != 'instructor':
        return redirect('inicio')
    return render(request, 'ontime_app/consultar_asistencias.html')

# Alertas (instructor)
@never_cache
@login_required(login_url='iniciar_sesion')
def alertas(request):
    if request.user.rol != 'instructor':
        return redirect('inicio')
    return render(request, 'ontime_app/alertas.html')

# Gestión de reportes (instructor)
@never_cache
@login_required(login_url='iniciar_sesion')
def gestion_reportes(request):
    if request.user.rol != 'instructor':
        return redirect('inicio')
    return render(request, 'ontime_app/gestion_reportes.html')

# Inicio general (sin login)
def inicio(request):
    return render(request, 'ontime_app/inicio.html')

# Contacto
def contacto(request):
    return render(request, 'ontime_app/contacto.html')

# Ayuda
def ayuda(request):
    return render(request, 'ontime_app/ayuda.html')

# Acerca de
def acerca_de(request):
    return render(request, 'ontime_app/acerca_de.html')

# Editar perfil 2 (aprendiz)
@never_cache
@login_required(login_url='iniciar_sesion')
def editar_perfil_2(request):
    usuario = request.user

    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            if form.cleaned_data['password']:
                usuario.set_password(form.cleaned_data['password'])
            form.save()
            return redirect('inicio_aprendiz')
    else:
        form = EditarPerfilForm(instance=usuario)

    return render(request, 'ontime_app/editar_perfil_2.html', {'form': form, 'usuario': usuario})

# Pantallas extra

def modelo_relacional(request):
    return render(request, 'ontime_app/modelo_relacional.html')

def normalizacion_mr(request):
    return render(request, 'ontime_app/normalizacion_mr.html')

def diccionario_datos(request):
    return render(request, 'ontime_app/diccionario_datos.html')

def diccionario_datoss(request):
    return render(request, 'ontime_app/diccionario_datoss.html')

def sentencias(request):
    return render(request, 'ontime_app/sentencias.html')

def diagrama_clases(request):
    return render(request, 'ontime_app/diagrama_clases.html')

# Pantalla admin

# Inicio admin
def es_admin(user):
    return user.is_authenticated and user.rol == 'admin'

@login_required(login_url='iniciar_sesion')
@user_passes_test(es_admin, login_url='iniciar_sesion')
def inicio_admin(request):
    form = RegistroForm()

    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Usuario creado correctamente!')
            return redirect('inicio_admin')

    return render(request, 'ontime_app/inicio_admin.html', {'form': form})

# Gestión usuarios (admin)
@never_cache
@login_required(login_url='iniciar_sesion')
def gestion_usuarios(request):
    if request.user.rol != 'admin':
        return redirect('inicio')
    return render(request, 'ontime_app/gestion_usuarios.html')

# Ver asistencias (admin)
@never_cache
@login_required(login_url='iniciar_sesion')
def ver_asistencias(request):
    if request.user.rol != 'admin':
        return redirect('inicio')
    return render(request, 'ontime_app/ver_asistencias.html')

# Gestión alertas (admin)
@never_cache
@login_required(login_url='iniciar_sesion')
def gestion_alertas(request):
    if request.user.rol != 'admin':
        return redirect('inicio')
    return render(request, 'ontime_app/gestion_alertas.html')

# Reportes (admin)
@never_cache
@login_required(login_url='iniciar_sesion')
def reportes(request):
    if request.user.rol != 'admin':
        return redirect('inicio')
    return render(request, 'ontime_app/reportes.html')

# Editar perfil admin
@never_cache
@login_required(login_url='iniciar_sesion')
def editar_perfil_adm(request):
    if request.user.rol != 'admin':
        return redirect('inicio')
    return render(request, 'ontime_app/editar_perfil_adm.html')

# Gestión horarios (admin)
@never_cache
@login_required(login_url='iniciar_sesion')
def gestion_horarios(request):
    if request.user.rol != 'admin':
        return redirect('inicio')
    return render(request, 'ontime_app/gestion_horarios.html')

# Control asistencia (admin)
@never_cache
@login_required(login_url='iniciar_sesion')
def control_asistencia(request):
    if request.user.rol != 'admin':
        return redirect('inicio')
    return render(request, 'ontime_app/control_asistencia.html')

# Carga masiva (admin)
@never_cache
@login_required(login_url='iniciar_sesion')
def carga_masiva(request):
    if request.user.rol != 'admin':
        return redirect('inicio')
    return render(request, 'ontime_app/carga_masiva.html')

# Historial (admin)
@never_cache
@login_required(login_url='iniciar_sesion')
def historial(request):
    if request.user.rol != 'admin':
        return redirect('inicio')
    return render(request, 'ontime_app/historial.html')

def es_admin(user):
    return user.is_authenticated and user.rol == 'admin'

# Crear usuarios (admin)
@login_required
@user_passes_test(es_admin)
def crear_usuario(request):
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

# Vistas para la página de registar asistencia
@login_required
def registrar_asistencia(request):
    if request.method == 'POST':
        codigo = request.POST.get('codigo')
        print("🔍 Código recibido:", codigo)

        if codigo == "ABC123":
            Asistencia.objects.create(
                aprendiz=request.user,
                codigo=codigo,
                fecha=timezone.now(),
                validada=True
            )
            return JsonResponse({'status': 'ok', 'msg': 'Asistencia registrada'})
        else:
            return JsonResponse({'status': 'error', 'msg': 'Código inválido'})

    return render(request, 'ontime_app/registrar_asistencia.html')