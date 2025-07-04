import os
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.conf import settings
from django.utils import timezone

# --- Modelo de Usuario Personalizado ---
class UsuarioPersonalizado(AbstractUser):
    ROLES = (
        ('aprendiz', 'Aprendiz'),
        ('instructor', 'Instructor'),
        ('admin', 'Administrador'),
    )

    rol = models.CharField(max_length=20, choices=ROLES)
    email = models.EmailField(unique=True)
    foto_perfil = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)

    clases = models.ManyToManyField('Clase', related_name="aprendices", blank=True)
    clases_dictadas = models.ManyToManyField('Clase', related_name="instructores", blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def save(self, *args, **kwargs):
        if self.email:
            self.email = self.email.lower()
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email

@receiver(post_delete, sender=UsuarioPersonalizado)
def eliminar_foto_perfil(sender, instance, **kwargs):
    if instance.foto_perfil and os.path.isfile(instance.foto_perfil.path):
        os.remove(instance.foto_perfil.path)

@receiver(pre_save, sender=UsuarioPersonalizado)
def eliminar_foto_anterior(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        anterior = UsuarioPersonalizado.objects.get(pk=instance.pk)
    except UsuarioPersonalizado.DoesNotExist:
        return
    if anterior.foto_perfil and anterior.foto_perfil != instance.foto_perfil:
        if os.path.isfile(anterior.foto_perfil.path):
            os.remove(anterior.foto_perfil.path)

# --- Modelo de Competencia ---
class Competencia(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

# --- Modelo de Clase ---
class Clase(models.Model):
    TIPOS_CLASE = (
        ('tecnica', 'Técnica'),
        ('complementaria', 'Complementaria'),
    )

    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPOS_CLASE)
    grupo = models.CharField(max_length=20)
    fecha = models.DateField()
    competencia = models.ForeignKey(Competencia, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = ('nombre', 'grupo')

    def __str__(self):
        return f"{self.nombre} - Grupo {self.grupo} ({self.get_tipo_display()})"

# --- Modelo de Asistencia ---
class Asistencia(models.Model):
    aprendiz = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    clase = models.ForeignKey(Clase, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=100)
    fecha = models.DateTimeField(default=timezone.now)
    validada = models.BooleanField(default=False)

    estado = models.CharField(
        max_length=20,
        choices=[
            ('Presente', 'Presente'),
            ('Ausente', 'Ausente'),
            ('Tarde', 'Tarde'),
            ('Justificado', 'Justificado')
        ],
        default='Presente'
    )
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Asistencia de {self.aprendiz.username} - {self.estado}"

# --- Modelo de Código Generado ---
class CodigoGenerado(models.Model):
    codigo = models.CharField(max_length=100, unique=True)
    instructor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    clase = models.ForeignKey(Clase, on_delete=models.CASCADE, null=True, blank=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.codigo} - {self.instructor.username}"

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

# --- Modelo de Notificación ---
class Notificacion(models.Model):
    TIPOS = [
        ('sistema', 'Del sistema'),
        ('instructor', 'De instructores'),
        ('asistencia', 'De registro de asistencias'),
    ]

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPOS)
    fecha = models.DateTimeField(auto_now_add=True)
    leida = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.titulo} - {self.usuario.username}"

# --- Modelo de Mensaje de contacto ---
class MensajeContacto(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    mensaje = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.correo}"

# --- Modelo de FAQ ---
class FAQ(models.Model):
    CATEGORIAS = [
        ('cuenta', 'Cuenta'),
        ('asistencia', 'Asistencia'),
        ('qr', 'QR'),
        ('reportes', 'Reportes'),
        ('otros', 'Otros'),
    ]

    pregunta = models.CharField(max_length=255)
    respuesta = models.TextField()
    categoria = models.CharField(max_length=20, choices=CATEGORIAS, default='otros')
    activa = models.BooleanField(default=True)

    def __str__(self):
        return self.pregunta

# --- Modelo de Alerta ---
class Alerta(models.Model):
    TIPO_CHOICES = [
        ('Inasistencia', 'Inasistencia'),
        ('Justificativo', 'Justificativo'),
        ('Retardo', 'Retardo'),
        ('Otro', 'Otro'),
    ]

    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Vista', 'Vista'),
        ('Resuelta', 'Resuelta'),
    ]

    aprendiz = models.ForeignKey(UsuarioPersonalizado, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    fecha = models.DateField(default=timezone.now)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Pendiente')
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.aprendiz.get_full_name()} - {self.tipo} - {self.estado}"

