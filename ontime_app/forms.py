from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.forms.widgets import FileInput
from .models import UsuarioPersonalizado


# Formulario para registro en el sistema
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


# Formulario para editar el perfil aprendiz
class EditarPerfilForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False)
    confirmar_password = forms.CharField(widget=forms.PasswordInput(), required=False)
    foto_perfil = forms.ImageField(
        required=False,
        widget=FileInput(attrs={
            'class': 'block w-full text-sm text-gray-600 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-green-50 file:text-green-700 hover:file:bg-green-100'
        })
    )

    class Meta:
        model = UsuarioPersonalizado
        fields = ['first_name', 'last_name', 'email', 'foto_perfil']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirmar = cleaned_data.get('confirmar_password')

        if password and password != confirmar:
            raise forms.ValidationError("Las contraseñas no coinciden.")


# Formulario para cambio de contraseña
class MiFormularioCambioContrasena(SetPasswordForm):
    nueva_contrasena = forms.CharField(label='Nueva contraseña', widget=forms.PasswordInput())
    repetir_contrasena = forms.CharField(label='Repetir contraseña', widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        pass1 = cleaned_data.get("nueva_contrasena")
        pass2 = cleaned_data.get("repetir_contrasena")
        if pass1 and pass2 and pass1 != pass2:
            self.add_error('repetir_contrasena', "Las contraseñas no coinciden.")
        return cleaned_data

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data["nueva_contrasena"])
        if commit:
            self.user.save()
        return self.user
