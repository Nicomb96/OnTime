from . import views
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import historial_api

urlpatterns = [

    # --- Rutas Generales ---
    path('', views.inicio, name="inicio"),
    path("contacto/", views.contacto, name="contacto"),
    path("usuarios/exportar_excel/", views.exportar_usuarios_excel, name="exportar_usuarios_excel"),
    path("ayuda/", views.ayuda, name="ayuda"),
    path("acerca_de/", views.acerca_de, name="acerca_de"),

    # --- Autenticación y Perfil ---
    path("iniciar_sesion/", views.iniciar_sesion, name="iniciar_sesion"),
    path("cambiar_contraseña/", views.cambiar_contraseña, name="cambiar_contraseña"),
    path("contraseña_actualizada/", views.contraseña_actualizada, name="contraseña_actualizada"),
    path('recuperar_contraseña/', views.recuperar_contraseña, name='recuperar_contraseña'),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),

    # --- Rutas de Perfil de Usuario ---
    path('editar-perfil/', views.editar_perfil, name='editar_perfil'),
    path('perfil/editar/', views.editar_perfil_unico, name='editar_perfil'),
    path('eliminar-foto/', views.eliminar_foto_perfil, name='eliminar_foto_perfil'),

    # --- Rol Aprendiz ---
    path("inicio_aprendiz/", views.inicio_aprendiz, name="inicio_aprendiz"),
    path("registrar_asistencia/", views.registrar_asistencia, name="registrar_asistencia"),
    path("notificaciones_1/", views.notificaciones_1, name="notificaciones_1"),
    path('historial-asistencia/cargar/', views.cargar_mas_historial, name='cargar_mas_historial'),
    path('api/historial/', historial_api, name='historial_api'),
    path('historial-asistencia/', views.historial_asistencia, name='historial_asistencia'),
    path('filtrar-asistencia/', views.filtrar_asistencia, name='filtrar_asistencia'),
    path('subir-justificativo/', views.subir_justificativo, name='subir_justificativo'),
    path('progreso-asistencia/', views.progreso_asistencia, name='progreso_asistencia'),
    path('notificaciones_1/leida/<int:id>/', views.marcar_notificacion_leida, name='marcar_notificacion_leida'),
    path('notificaciones_1/eliminar/<int:id>/', views.eliminar_notificacion, name='eliminar_notificacion'),
    path('notificaciones_1/filtrar/', views.filtrar_notificaciones, name='filtrar_notificaciones'),
    path('notificaciones_1/cargar_mas/', views.cargar_mas_notificaciones, name='cargar_mas_notificaciones'),

    # --- Rol Instructor ---
    path("inicio_instructor/", views.inicio_instructor, name="inicio_instructor"),
    path("generar_qr/", views.generar_qr, name="generar_qr"),
    path("consultar_asistencias/", views.consultar_asistencias, name="consultar_asistencias"),
    path("alertas/", views.alertas, name="alertas"),
    path("gestion_reportes/", views.gestion_reportes, name="gestion_reportes"),

    # --- Rol Administrador ---
    path("inicio_admin/", views.inicio_admin, name="inicio_admin"), 
    path("gestion_usuarios/", views.gestion_usuarios, name="gestion_usuarios"),
    path("filtrar_usuarios_ajax/", views.filtrar_usuarios_ajax, name="filtrar_usuarios_ajax"),
    path("ver_asistencias/", views.ver_asistencias, name="ver_asistencias"),
    path("gestion_alertas/", views.gestion_alertas, name="gestion_alertas"),
    path("reportes/", views.reportes, name="reportes"),
    path("gestion_horarios/", views.gestion_horarios, name="gestion_horarios"),
    path("control_asistencia/", views.control_asistencia, name="control_asistencia"),
    path("carga_masiva/", views.carga_masiva, name="carga_masiva"),
    path("historial/", views.historial_1, name="historial"),
    path("crear_usuario/", views.crear_usuario, name="crear_usuario"),
    path("usuarios/editar/<int:id>/", views.editar_usuario, name="editar_usuario"),  # ✅ Paso 4
    path("usuarios/eliminar/<int:id>/", views.eliminar_usuario, name="eliminar_usuario"),  # ✅ Paso 4

    # --- Extras (documentación, diseño) ---
    path("modelo_relacional/", views.modelo_relacional, name="modelo_relacional"),
    path("normalizacion_mr/", views.normalizacion_mr, name="normalizacion_mr"),
    path("diccionario_datos/", views.diccionario_datos, name="diccionario_datos"),
    path("diccionario_datoss/", views.diccionario_datoss, name="diccionario_datoss"),
    path("sentencias/", views.sentencias, name="sentencias"),
    path("diagrama_clases/", views.diagrama_clases, name="diagrama_clases"),

    # --- Recuperación de Contraseña ---
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
