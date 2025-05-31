from django.shortcuts import render, redirect
from .forms import RegistroForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from .models import UsuarioPersonalizado
from django.contrib.auth.decorators import login_required

# Vista para iniciar sesión
def iniciar_sesion(request):
    return render(request, 'ontime_app/iniciar_sesion.html')

# Vista para registrarse
def registrarse(request):
    return render(request, 'ontime_app/registrarse.html')

# Vista para recuperar la contraseña
def recuperar_contraseña(request):
    return render(request, 'ontime_app/recuperar_contraseña.html')

# Vista para cambiar la contraseña
def cambiar_contraseña(request):
    return render(request, 'ontime_app/cambiar_contraseña.html')

# Vista para mostrar mensaje de contraseña actualizada
def contraseña_actualizada(request):
    return render(request, 'ontime_app/contraseña_actualizada.html')

# Vista para la página de inicio del aprendiz
def inicio_aprendiz(request):
    return render(request, 'ontime_app/inicio_aprendiz.html')

# Vista para la página de registrar asistencia QR
def registrar_asistencia(request):
    return render(request, 'ontime_app/registrar_asistencia.html')

# Vista para la página de notificaciones
def notificaciones_1(request):
    return render(request, 'ontime_app/notificaciones_1.html')

# Vista para la página de historial
def historial_1(request):
    return render(request, 'ontime_app/historial_1.html')

# Vista para la página de justificativos
def justificativos_1(request):
    return render(request, 'ontime_app/justificativos_1.html')

# Vista para la página de editar perfil 1
def editar_perfil_1(request):
    return render(request, 'ontime_app/editar_perfil_1.html')

# Vista para la página de inicio del instructor
def inicio_instructor(request):
    return render(request, 'ontime_app/inicio_instructor.html')

# Vista para la página de generar qr
def generar_qr(request):
    return render(request, 'ontime_app/generar_qr.html')

# Vista para la página de consultar asistencias
def consultar_asistencias(request):
    return render(request, 'ontime_app/consultar_asistencias.html')

# Vista para la página de alertas
def alertas(request):
    return render(request, 'ontime_app/alertas.html')

# Vista para la página de gestion de reportes
def gestion_reportes(request):
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
def editar_perfil_2(request):
    return render(request, 'ontime_app/editar_perfil_2.html')

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
def inicio_admin(request):
    return render(request, 'ontime_app/inicio_admin.html')

# vista para la página de gestion de usuarios
def gestion_usuarios(request):
    return render(request, 'ontime_app/gestion_usuarios.html')

# vista para la página de ver asistencias
def ver_asistencias(request):
    return render(request, 'ontime_app/ver_asistencias.html')

# vista para la página de gestion de alertas
def gestion_alertas(request):
    return render(request, 'ontime_app/gestion_alertas.html')

# vista para la página de reportes
def reportes(request):
    return render(request, 'ontime_app/reportes.html')

# vista para la página editar perfil admin
def editar_perfil_adm(request):
    return render(request, 'ontime_app/editar_perfil_adm.html')

# vista para la página gestion de horarios
def gestion_horarios(request):
    return render(request, 'ontime_app/gestion_horarios.html')

# vista para la página de control de asistencia
def control_asistencia(request):
    return render(request, 'ontime_app/control_asistencia.html')

# vista para la página de cargar masiva
def carga_masiva(request):
    return render(request, 'ontime_app/carga_masiva.html')

# vista para la página de historial
def historial(request):
    return render(request, 'ontime_app/historial.html')


# Vistas CRUD:

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

@login_required
def vista_aprendiz(request):
    return render(request, 'ontime_app/inicio_aprendiz.html')

@login_required
def vista_instructor(request):
    return render(request, 'ontime_app/inicio_instructor.html')

@login_required
def vista_admin(request):
    return render(request, 'ontime_app/inicio_admin.html')


