from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from .models import UsuarioPersonalizado
import os

@receiver(post_delete, sender=UsuarioPersonalizado)
def borrar_foto_al_borrar_usuario(sender, instance, **kwargs):
    # Cuando borran un usuario, borra la foto de perfil si existe
    if instance.foto_perfil:
        if os.path.isfile(instance.foto_perfil.path):
            os.remove(instance.foto_perfil.path)

@receiver(pre_save, sender=UsuarioPersonalizado)
def borrar_foto_vieja_al_actualizar(sender, instance, **kwargs):
    # Cuando actualizan la foto de perfil, borra la vieja para no llenar el disco
    if not instance.pk:
        return  # Si es un usuario nuevo, no hay vieja foto que borrar

    try:
        old_usuario = UsuarioPersonalizado.objects.get(pk=instance.pk)
    except UsuarioPersonalizado.DoesNotExist:
        return

    old_foto = old_usuario.foto_perfil
    nueva_foto = instance.foto_perfil

    if old_foto and old_foto != nueva_foto:
        if os.path.isfile(old_foto.path):
            os.remove(old_foto.path)