from django.contrib.auth.models import AbstractUser
from django.db import models

class UsuarioPersonalizado(AbstractUser):
    ROLES = (
        ('aprendiz', 'Aprendiz'),
        ('instructor', 'Instructor'),
        ('admin', 'Administrador'),
    )
    rol = models.CharField(max_length=20, choices=ROLES)

    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.email
