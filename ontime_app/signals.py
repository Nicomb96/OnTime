import os
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from .models import UsuarioPersonalizado

# Conecta esta función a la señal post_delete (después de borrar) del modelo UsuarioPersonalizado
@receiver(post_delete, sender=UsuarioPersonalizado)
def borrar_foto_al_borrar_usuario(sender, instance, **kwargs):
    """
    Elimina la foto de perfil del sistema de archivos cuando un usuario es borrado.
    Esto evita que queden archivos "huérfanos" que ocupen espacio innecesario.
    """
    # Verifica si el usuario tenía una foto de perfil asignada
    if instance.foto_perfil:
        # Comprueba si el archivo de la foto realmente existe en la ruta especificada
        if os.path.isfile(instance.foto_perfil.path):
            # Si existe, procede a eliminar el archivo físico
            os.remove(instance.foto_perfil.path)

# Conecta esta función a la señal pre_save (antes de guardar) del modelo UsuarioPersonalizado
@receiver(pre_save, sender=UsuarioPersonalizado)
def borrar_foto_vieja_al_actualizar(sender, instance, **kwargs):
    """
    Elimina la foto de perfil antigua del sistema de archivos cuando un usuario
    actualiza su foto por una nueva. Esto previene la acumulación de archivos
    de fotos antiguas y ahorra espacio en disco.
    """
    # Si el usuario es nuevo (no tiene Primary Key aún), no hay foto vieja que borrar
    if not instance.pk:
        return

    try:
        # Intenta obtener la versión antigua del usuario desde la base de datos
        old_usuario = UsuarioPersonalizado.objects.get(pk=instance.pk)
    except UsuarioPersonalizado.DoesNotExist:
        # Si el usuario no existe en la base de datos (raro en un pre_save de un PK existente), no hay nada que hacer
        return

    # Obtiene la foto de perfil que tenía el usuario antes de la actualización
    old_foto = old_usuario.foto_perfil
    # Obtiene la nueva foto de perfil que se va a guardar
    nueva_foto = instance.foto_perfil

    # Comprueba si había una foto antigua y si la nueva foto es diferente a la antigua
    if old_foto and old_foto != nueva_foto:
        # Si el archivo de la foto antigua existe en el sistema de archivos
        if os.path.isfile(old_foto.path):
            # Elimina el archivo físico de la foto antigua
            os.remove(old_foto.path)
