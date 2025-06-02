from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("iniciar_sesion/", views.iniciar_sesion, name="iniciar_sesion"),
    path("registrarse/", views.registrarse, name="registrarse"),
    path("cambiar_contraseña/", views.cambiar_contraseña, name="cambiar_contraseña"),
    path("contraseña_actualizada/", views.contraseña_actualizada, name="contraseña_actualizada"),
    path("inicio_aprendiz/", views.inicio_aprendiz, name="inicio_aprendiz"),
    path("registrar_asistencia/", views.registrar_asistencia, name="registrar_asistencia"),
    path("notificaciones_1/", views.notificaciones_1, name="notificaciones_1"),
    path("historial_1/", views.historial_1, name="historial_1"),
    path("justificativos_1/", views.justificativos_1, name="justificativos_1"),
    path("editar_perfil_1/", views.editar_perfil_1, name="editar_perfil_1"),
    path("inicio_instructor/", views.inicio_instructor, name="inicio_instructor"),
    path("generar_qr/", views.generar_qr, name="generar_qr"),
    path("consultar_asistencias/", views.consultar_asistencias, name="consultar_asistencias"),
    path("alertas/", views.alertas, name="alertas"),
    path("gestion_reportes/", views.gestion_reportes, name="gestion_reportes"),
    path('', views.inicio, name="inicio"),
    path("contacto/", views.contacto, name="contacto"),
    path("ayuda/", views.ayuda, name="ayuda"),
    path("acerca_de/", views.acerca_de, name="acerca_de"),
    path("editar_perfil_2/", views.editar_perfil_2, name="editar_perfil_2"),
    path('recuperar_contraseña/', views.recuperar_contraseña, name='recuperar_contraseña'),

    # Pantallas extra en el sistema
    
    path("modelo_relacional/", views.modelo_relacional, name="modelo_relacional"),
    path("normalizacion_mr/", views.normalizacion_mr, name="normalizacion_mr"),
    path("diccionario_datos/", views.diccionario_datos, name="diccionario_datos"),
    path("diccionario_datoss/", views.diccionario_datoss, name="diccionario_datoss"),
    path("sentencias/", views.sentencias, name="sentencias"),
    path("diagrama_clases/", views.diagrama_clases, name="diagrama_clases"),

    # Pantallas admin

    path("inicio_admin/", views.inicio_admin, name="inicio_admin"),
    path("gestion_usuarios/", views.gestion_usuarios, name="gestion_usuarios"),
    path("ver_asistencias/", views.ver_asistencias, name="ver_asistencias"),
    path("gestion_alertas/", views.gestion_alertas, name="gestion_alertas"),
    path("reportes/", views.reportes, name="reportes"),
    path("editar_perfil_adm/", views.editar_perfil_adm, name="editar_perfil_adm"),
    path("gestion_horarios/", views.gestion_horarios, name="gestion_horarios"),
    path("control_asistencia/", views.control_asistencia, name="control_asistencia"),
    path("carga_masiva/", views.carga_masiva, name="carga_masiva"),
    path("historial/", views.historial, name="historial"),

    # Cerrae sesión
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),

    # Eliminar foto de perfil
    path('eliminar-foto/', views.eliminar_foto_perfil, name='eliminar_foto_perfil'),

    # Vista que manda el correo
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='ontime_app/recuperar_contraseña.html',
        email_template_name='registration/password_reset_email.html',
        subject_template_name='registration/password_reset_subject.txt',
        success_url='/password_reset/done/'
    ), name='password_reset'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='ontime_app/registration/password_reset_done.html'
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='ontime_app/registration/password_reset_confirm.html',
        success_url='/reset/done/'
    ), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='ontime_app/registration/password_reset_complete.html'
    ), name='password_reset_complete'),
]