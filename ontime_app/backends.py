from django.contrib.auth.backends import ModelBackend
from .models import UsuarioPersonalizado

class EmailBackend(ModelBackend):
    """
    Backend de autenticación personalizado que permite iniciar sesión usando el correo electrónico
    en lugar del nombre de usuario predeterminado de Django.
    """
    def authenticate(self, request, email=None, password=None, **kwargs):
        """
        Método principal para autenticar a un usuario.
        Intenta encontrar un usuario por email y verificar su contraseña.
        """
        # Si no se proporciona email o contraseña, no se puede autenticar
        if email is None or password is None:
            return None

        try:
            # Intenta obtener un usuario de tu modelo personalizado que coincida con el email
            user = UsuarioPersonalizado.objects.get(email=email)
        except UsuarioPersonalizado.DoesNotExist:
            # Si no se encuentra un usuario con ese email, la autenticación falla
            return None

        # Verifica si la contraseña proporcionada es correcta para el usuario encontrado
        # y si el usuario está activo y puede ser autenticado (método de ModelBackend)
        if user.check_password(password) and self.user_can_authenticate(user):
            return user # Retorna el objeto de usuario si la autenticación es exitosa
        
        # Si la contraseña no coincide o el usuario no puede ser autenticado, retorna None
        return None
