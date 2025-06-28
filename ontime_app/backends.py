from django.contrib.auth.backends import ModelBackend
from .models import UsuarioPersonalizado

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, email=None, password=None, **kwargs):
        email = email or username
        if email is None or password is None:
            return None
        try:
            user = UsuarioPersonalizado.objects.get(email=email)
        except UsuarioPersonalizado.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
