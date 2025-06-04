from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
import os


class UsuarioPersonalizado(AbstractUser):
    # Define los roles posibles para el usuario
    ROLES = (
        ('aprendiz', 'Aprendiz'),
        ('instructor', 'Instructor'),
        ('admin', 'Administrador'),
    )
    rol = models.CharField(max_length=20, choices=ROLES)

    email = models.EmailField(unique=True)
    foto_perfil = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.email


# Señal para borrar la foto de perfil cuando se elimina el usuario del sistema
@receiver(post_delete, sender=UsuarioPersonalizado)
def eliminar_foto_perfil(sender, instance, **kwargs):
    if instance.foto_perfil:
        if os.path.isfile(instance.foto_perfil.path):
            os.remove(instance.foto_perfil.path)


# Señal para borrar la foto anterior cuando se actualiza la foto de perfil
@receiver(pre_save, sender=UsuarioPersonalizado)
def eliminar_foto_anterior(sender, instance, **kwargs):
    if not instance.pk:
        return  # Es nuevo, no hay foto anterior que borrar

    try:
        usuario_anterior = UsuarioPersonalizado.objects.get(pk=instance.pk)
    except UsuarioPersonalizado.DoesNotExist:
        return

    foto_anterior = usuario_anterior.foto_perfil
    nueva_foto = instance.foto_perfil

    if foto_anterior and foto_anterior != nueva_foto:
        if os.path.isfile(foto_anterior.path):
            os.remove(foto_anterior.path)
