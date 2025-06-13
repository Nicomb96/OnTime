import os
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.conf import settings
from datetime import datetime

# --- Modelo de Usuario Personalizado ---

class UsuarioPersonalizado(AbstractUser):
    """
    Define un modelo de usuario personalizado que extiende AbstractUser.
    Permite añadir campos adicionales como el rol y la foto de perfil.
    """
    # Define las opciones de roles disponibles para los usuarios
    ROLES = (
        ('aprendiz', 'Aprendiz'),
        ('instructor', 'Instructor'),
        ('admin', 'Administrador'),
    )
    # Campo para almacenar el rol del usuario, con opciones predefinidas
    rol = models.CharField(max_length=20, choices=ROLES)

    # Campo de correo electrónico, se asegura que sea único
    email = models.EmailField(unique=True)
    # Campo para la foto de perfil, se guarda en 'fotos_perfil/' y es opcional
    foto_perfil = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)

    # Define 'email' como el campo usado para iniciar sesión
    USERNAME_FIELD = 'email'
    # Define los campos requeridos al crear un superusuario o usuario
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        """
        Representación en cadena del objeto UsuarioPersonalizado, muestra el email.
        """
        return self.email

# --- Señales para el Modelo UsuarioPersonalizado ---

@receiver(post_delete, sender=UsuarioPersonalizado)
def eliminar_foto_perfil(sender, instance, **kwargs):
    """
    Señal que se ejecuta después de que un UsuarioPersonalizado es eliminado.
    Elimina la foto de perfil asociada del sistema de archivos para evitar archivos huérfanos.
    """
    # Verifica si el usuario tenía una foto de perfil
    if instance.foto_perfil:
        # Comprueba si el archivo físico de la foto existe
        if os.path.isfile(instance.foto_perfil.path):
            # Elimina el archivo físico del sistema
            os.remove(instance.foto_perfil.path)

@receiver(pre_save, sender=UsuarioPersonalizado)
def eliminar_foto_anterior(sender, instance, **kwargs):
    """
    Señal que se ejecuta antes de guardar un UsuarioPersonalizado.
    Si se está actualizando la foto de perfil, elimina la foto antigua del sistema de archivos.
    """
    # Si el usuario es nuevo (no tiene PK), no hay foto anterior que borrar
    if not instance.pk:
        return

    try:
        # Intenta obtener la versión existente del usuario de la base de datos
        usuario_anterior = UsuarioPersonalizado.objects.get(pk=instance.pk)
    except UsuarioPersonalizado.DoesNotExist:
        # Si el usuario no existe, no hay foto anterior que borrar
        return

    # Obtiene la foto de perfil que el usuario tenía antes de la actualización
    foto_anterior = usuario_anterior.foto_perfil
    # Obtiene la nueva foto de perfil que se va a guardar
    nueva_foto = instance.foto_perfil

    # Si había una foto anterior y es diferente a la nueva foto
    if foto_anterior and foto_anterior != nueva_foto:
        # Comprueba si el archivo físico de la foto anterior existe
        if os.path.isfile(foto_anterior.path):
            # Elimina el archivo físico de la foto anterior
            os.remove(foto_anterior.path)

# --- Modelo de Asistencia ---

class Asistencia(models.Model):
    aprendiz = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=100)
    fecha = models.DateTimeField(default=datetime.now)
    validada = models.BooleanField(default=False)
    clase = models.ForeignKey('Clase', on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"Asistencia de {self.aprendiz.username} - {self.codigo}"

# --- Modelo de Notificación ---

class Notificacion(models.Model):
    """
    Modelo para gestionar notificaciones enviadas a los usuarios.
    """
    # Define los tipos de notificaciones posibles
    TIPOS = [
        ('sistema', 'Del sistema'),
        ('instructor', 'De instructores'),
        ('asistencia', 'De registro de asistencias'),
    ]

    # Clave foránea al modelo de usuario, se eliminan las notificaciones si se elimina el usuario
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # Título de la notificación
    titulo = models.CharField(max_length=255)
    # Contenido de la notificación
    descripcion = models.TextField()
    # Tipo de notificación, con opciones predefinidas
    tipo = models.CharField(max_length=20, choices=TIPOS)
    # Fecha y hora de creación de la notificación, se establece automáticamente
    fecha = models.DateTimeField(auto_now_add=True)
    # Indica si la notificación ha sido leída por el usuario
    leida = models.BooleanField(default=False)

    def __str__(self):
        """
        Representación en cadena del objeto Notificacion.
        """
        return f"{self.titulo} - {self.usuario.username}"

# --- Modelo de Justificativo ---

class Justificativo(models.Model):
    TIPO_CHOICES = [
        ('medico', 'Médico'),
        ('personal', 'Personal'),
        ('familia', 'Familiar'),
        ('otro', 'Otro'),
    ]

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    fecha_ausencia = models.DateField()
    descripcion = models.TextField()
    archivo = models.FileField(upload_to='justificativos/')
    fecha_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.tipo} ({self.fecha_ausencia})"

# --- Modelo de Clase ---

class Clase(models.Model):
    nombre = models.CharField(max_length=100)
    fecha = models.DateField()

    def __str__(self):
        return f"{self.nombre} - {self.fecha}"
