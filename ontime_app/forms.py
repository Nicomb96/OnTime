from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.forms.widgets import FileInput
from .models import UsuarioPersonalizado

# --- Formulario para el Registro de Usuarios ---

class RegistroForm(UserCreationForm):
    """
    Formulario para registrar nuevos usuarios en el sistema.
    Extiende UserCreationForm para manejar la creación de usuarios con contraseña.
    """
    # Campos adicionales para el registro
    nombre = forms.CharField(label='Nombre')  # Campo para el nombre del usuario
    apellido = forms.CharField(label='Apellido')  # Campo para el apellido del usuario
    correo = forms.EmailField(label='Correo Electrónico')  # Campo para el correo electrónico (será el USERNAME_FIELD)
    rol = forms.ChoiceField(choices=UsuarioPersonalizado.ROLES, label='Rol')  # Campo para seleccionar el rol del usuario

    class Meta:
        """
        Clase Meta para configurar el formulario.
        """
        model = UsuarioPersonalizado  # Asocia el formulario con el modelo UsuarioPersonalizado
        # Define los campos que se mostrarán en el formulario de registro
        fields = ['username', 'nombre', 'apellido', 'correo', 'rol', 'password1', 'password2']

    def save(self, commit=True):
        """
        Guarda el nuevo usuario, asignando los campos personalizados.
        """
        # Llama al save del formulario padre (UserCreationForm) pero sin guardar aún en la DB
        user = super().save(commit=False)
        # Asigna los datos limpios de los campos adicionales al modelo de usuario
        user.first_name = self.cleaned_data['nombre']
        user.last_name = self.cleaned_data['apellido']
        user.email = self.cleaned_data['correo']
        user.rol = self.cleaned_data['rol']
        # Si commit es True, guarda el usuario en la base de datos
        if commit:
            user.save()
        return user

# --- Formulario para Editar el Perfil del Usuario ---

class EditarPerfilForm(forms.ModelForm):
    """
    Formulario para permitir a los usuarios (ej. aprendices) editar su perfil.
    Incluye campos para cambiar contraseña y subir foto de perfil.
    """
    # Campo opcional para cambiar la contraseña
    password = forms.CharField(widget=forms.PasswordInput(), required=False, label='Nueva Contraseña')
    # Campo opcional para confirmar la nueva contraseña
    confirmar_password = forms.CharField(widget=forms.PasswordInput(), required=False, label='Confirmar Contraseña')
    # Campo para subir la foto de perfil, con un widget personalizado para estilizado
    foto_perfil = forms.ImageField(
        required=False,
        label='Foto de Perfil',
        widget=FileInput(attrs={
            # Clases CSS para estilizar el input de archivo
            'class': 'block w-full text-sm text-gray-600 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-green-50 file:text-green-700 hover:file:bg-green-100'
        })
    )

    class Meta:
        """
        Clase Meta para configurar el formulario.
        """
        model = UsuarioPersonalizado  # Asocia el formulario con el modelo UsuarioPersonalizado
        # Define los campos del modelo que se incluirán en el formulario
        fields = ['first_name', 'last_name', 'email', 'foto_perfil']

    def clean(self):
        """
        Método para validar los datos del formulario, especialmente las contraseñas.
        """
        # Llama al método clean del padre para obtener los datos validados
        cleaned_data = super().clean()
        password = cleaned_data.get('password')  # Obtiene la nueva contraseña
        confirmar = cleaned_data.get('confirmar_password')  # Obtiene la confirmación de la contraseña

        # Si se ingresó una nueva contraseña y no coincide con la confirmación, lanza un error
        if password and password != confirmar:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned_data

# --- Formulario para el Cambio de Contraseña (desde recuperación) ---

class MiFormularioCambioContrasena(SetPasswordForm):
    """
    Formulario para cambiar la contraseña del usuario después de una recuperación
    o restablecimiento. Extiende SetPasswordForm.
    """
    # Campos para la nueva contraseña y su repetición
    nueva_contrasena = forms.CharField(label='Nueva contraseña', widget=forms.PasswordInput())
    repetir_contrasena = forms.CharField(label='Repetir contraseña', widget=forms.PasswordInput())

    def clean(self):
        """
        Método para validar que las dos contraseñas ingresadas coincidan.
        """
        # Llama al método clean del padre para validaciones básicas
        cleaned_data = super().clean()
        pass1 = cleaned_data.get("nueva_contrasena")  # Obtiene la primera entrada de contraseña
        pass2 = cleaned_data.get("repetir_contrasena")  # Obtiene la segunda entrada de contraseña
        # Si ambas contraseñas están presentes y no coinciden, agrega un error
        if pass1 and pass2 and pass1 != pass2:
            self.add_error('repetir_contrasena', "Las contraseñas no coinciden.")
        return cleaned_data

    def save(self, commit=True):
        """
        Guarda la nueva contraseña para el usuario.
        """
        # Establece la nueva contraseña en el objeto de usuario asociado al formulario
        self.user.set_password(self.cleaned_data["nueva_contrasena"])
        # Si commit es True, guarda el usuario en la base de datos
        if commit:
            self.user.save()
        return self.user