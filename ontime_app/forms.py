from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UsuarioPersonalizado

class RegistroForm(UserCreationForm):
    nombre = forms.CharField()
    apellido = forms.CharField()
    correo = forms.EmailField()
    rol = forms.ChoiceField(choices=UsuarioPersonalizado.ROLES)

    class Meta:
        model = UsuarioPersonalizado
        fields = ['username', 'nombre', 'apellido', 'correo', 'rol', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['nombre']
        user.last_name = self.cleaned_data['apellido']
        user.email = self.cleaned_data['correo']
        user.rol = self.cleaned_data['rol']
        if commit:
            user.save()
        return user
