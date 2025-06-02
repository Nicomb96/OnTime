import os
from .forms import RegistroForm, EditarPerfilForm, MiFormularioCambioContrasena
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth import logout
from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.utils.encoding import force_str

# Vista para iniciar sesión
def iniciar_sesion(request):
    if request.method == 'POST':
        correo = request.POST.get('correo')
        contrasena = request.POST.get('contrasena')

        user = authenticate(request, email=correo, password=contrasena)

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
                messages.error(request, 'Rol desconocido, contacta al admin.')
        else:
            messages.error(request, 'Correo o contraseña incorrectos.')

        return render(request, 'ontime_app/iniciar_sesion.html', {'correo': correo})

    return render(request, 'ontime_app/iniciar_sesion.html')

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
    return redirect('iniciar_sesion')

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
    template_name = 'recuperar_contraseña_confirm.html'  # Aquí usas tu template

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
            return render(request, 'password_reset_invalid.html')  # Ponle una plantilla para token inválido

    def post(self, request, uidb64=None, token=None):
        user = self.get_user(uidb64)
        if user is not None and default_token_generator.check_token(user, token):
            form = MiFormularioCambioContrasena(user=user, data=request.POST)
            if form.is_valid():
                form.save()
                return redirect('contraseña_actualizada')  # O a donde quieras mandar
            else:
                return render(request, self.template_name, {'form': form})
        else:
            return render(request, 'password_reset_invalid.html')
        
# Vista para cambiar contraseña
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

# Vista para cambiar la contraseña
def cambiar_contraseña(request):
    return render(request, 'ontime_app/cambiar_contraseña.html')

# Vista contraseña actualizada
def contraseña_actualizada(request):
    return render(request, 'ontime_app/contraseña_actualizada.html')

# Vista para la página de inicio del aprendiz
@never_cache
@login_required(login_url='iniciar_sesion')
def inicio_aprendiz(request):
    if request.user.rol != 'aprendiz':
        return redirect('inicio')  # Lo sacamos si no es aprendiz
    usuario = request.user  # Obtenemos el usuario actual
    return render(request, 'ontime_app/inicio_aprendiz.html', {
        'usuario': usuario  # Lo mandamos al template
    })

# Vista para la página de registrar asistencia QR
@never_cache
@login_required(login_url='iniciar_sesion')
def registrar_asistencia(request):
    if request.user.rol != 'aprendiz':
        return redirect('inicio')
    return render(request, 'ontime_app/registrar_asistencia.html')

# Vista para la página de notificaciones
@never_cache
@login_required(login_url='iniciar_sesion')
def notificaciones_1(request):
    if request.user.rol != 'aprendiz':
        return redirect('inicio')
    return render(request, 'ontime_app/notificaciones_1.html')

# Vista para la página de historial
@never_cache
@login_required(login_url='iniciar_sesion')
def historial_1(request):
    if request.user.rol != 'aprendiz':
        return redirect('inicio')
    return render(request, 'ontime_app/historial_1.html')

# Vista para la página de justificativos
@never_cache
@login_required(login_url='iniciar_sesion')
def justificativos_1(request):
    if request.user.rol != 'aprendiz':
        return redirect('inicio')
    return render(request, 'ontime_app/justificativos_1.html')

# Vista para la página de editar perfil 1
@never_cache
@login_required(login_url='iniciar_sesion')
def editar_perfil_1(request):
    if request.user.rol != 'aprendiz':
        return redirect('inicio')
    return render(request, 'ontime_app/editar_perfil_1.html')

# Vista para la página de inicio del instructor
@never_cache
@login_required(login_url='iniciar_sesion')
def inicio_instructor(request):
    if request.user.rol != 'instructor':
        return redirect('inicio')
    return render(request, 'ontime_app/inicio_instructor.html')

# Vista para la página de generar qr
@never_cache
@login_required(login_url='iniciar_sesion')
def generar_qr(request):
    if request.user.rol != 'instructor':
        return redirect('inicio')
    return render(request, 'ontime_app/generar_qr.html')

# Vista para la página de consultar asistencias
@never_cache
@login_required(login_url='iniciar_sesion')
def consultar_asistencias(request):
    if request.user.rol != 'instructor':
        return redirect('inicio')
    return render(request, 'ontime_app/consultar_asistencias.html')

# Vista para la página de alertas
@never_cache
@login_required(login_url='iniciar_sesion')
def alertas(request):
    if request.user.rol != 'instructor':
        return redirect('inicio')
    return render(request, 'ontime_app/alertas.html')

# Vista para la página de gestion de reportes
@never_cache
@login_required(login_url='iniciar_sesion')
def gestion_reportes(request):
    if request.user.rol != 'instructor':
        return redirect('inicio')
    return render(request, 'ontime_app/gestion_reportes.html')

# Vista para la página de inicio
def inicio(request):
    return render(request, 'ontime_app/inicio.html')

# Vista para la página de contacto
def contacto(request):
    return render(request, 'ontime_app/contacto.html')

# Vista para la página de ayuda
def ayuda(request):
    return render(request, 'ontime_app/ayuda.html')

# Vista para la página de acerca de
def acerca_de(request):
    return render(request, 'ontime_app/acerca_de.html')

# Vista para la página de editar perfil 2
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

# Patallas extra en el sistema

# Vista para la página de modelo relacional
def modelo_relacional(request):
    return render(request, 'ontime_app/modelo_relacional.html')

# Vista para la página de normalizacion del MR
def normalizacion_mr(request):
    return render(request, 'ontime_app/normalizacion_mr.html')

# Vista para la página de diccionario datos
def diccionario_datos(request):
    return render(request, 'ontime_app/diccionario_datos.html')

# Vista para la página de diccionario datoss
def diccionario_datoss(request):
    return render(request, 'ontime_app/diccionario_datoss.html')

# Vista para la página de sentencias DDL Y DML
def sentencias(request):
    return render(request, 'ontime_app/sentencias.html')

# Vista para la página de diagrama de clases
def diagrama_clases(request):
    return render(request, 'ontime_app/diagrama_clases.html')

# Pantalla admin

# vista para la página de inicio del administrador
@never_cache
@login_required(login_url='iniciar_sesion')
def inicio_admin(request):
    if request.user.rol != 'admin':
        return redirect('inicio')
    return render(request, 'ontime_app/inicio_admin.html')

# vista para la página de gestion de usuarios
@never_cache
@login_required(login_url='iniciar_sesion')
def gestion_usuarios(request):
    if request.user.rol != 'admin':
        return redirect('inicio')
    return render(request, 'ontime_app/gestion_usuarios.html')

# vista para la página de ver asistencias
@never_cache
@login_required(login_url='iniciar_sesion')
def ver_asistencias(request):
    if request.user.rol != 'admin':
        return redirect('inicio')
    return render(request, 'ontime_app/ver_asistencias.html')

# vista para la página de gestion de alertas
@never_cache
@login_required(login_url='iniciar_sesion')
def gestion_alertas(request):
    if request.user.rol != 'admin':
        return redirect('inicio')
    return render(request, 'ontime_app/gestion_alertas.html')

# vista para la página de reportes
@never_cache
@login_required(login_url='iniciar_sesion')
def reportes(request):
    if request.user.rol != 'admin':
        return redirect('inicio')
    return render(request, 'ontime_app/reportes.html')

# vista para la página editar perfil admin
@never_cache
@login_required(login_url='iniciar_sesion')
def editar_perfil_adm(request):
    if request.user.rol != 'admin':
        return redirect('inicio')
    return render(request, 'ontime_app/editar_perfil_adm.html')

# vista para la página gestion de horarios
@never_cache
@login_required(login_url='iniciar_sesion')
def gestion_horarios(request):
    if request.user.rol != 'admin':
        return redirect('inicio')
    return render(request, 'ontime_app/gestion_horarios.html')

# vista para la página de control de asistencia
@never_cache
@login_required(login_url='iniciar_sesion')
def control_asistencia(request):
    if request.user.rol != 'admin':
        return redirect('inicio')
    return render(request, 'ontime_app/control_asistencia.html')

# vista para la página de cargar masiva
@never_cache
@login_required(login_url='iniciar_sesion')
def carga_masiva(request):
    if request.user.rol != 'admin':
        return redirect('inicio')
    return render(request, 'ontime_app/carga_masiva.html')

# vista para la página de historial
@never_cache
@login_required(login_url='iniciar_sesion')
def historial(request):
    if request.user.rol != 'admin':
        return redirect('inicio')
    return render(request, 'ontime_app/historial.html')