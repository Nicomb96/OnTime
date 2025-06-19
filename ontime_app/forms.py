from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.forms.widgets import FileInput
from .models import UsuarioPersonalizado
from .models import Justificativo
from django.contrib.auth import get_user_model
from django.forms import FileInput
from django.contrib.auth import authenticate, login

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
    Formulario para permitir a los usuarios editar su perfil.
    Incluye validaciones para contraseña, foto, etc.
    """
    password = forms.CharField(widget=forms.PasswordInput(), required=False, label='Nueva Contraseña')
    confirmar_password = forms.CharField(widget=forms.PasswordInput(), required=False, label='Confirmar Contraseña')

    foto_perfil = forms.ImageField(
        required=False,
        label='Foto de Perfil',
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

        return cleaned_data

    def clean_foto_perfil(self):
        foto = self.cleaned_data.get('foto_perfil')
        # Solo si se subió una nueva imagen
        if foto and hasattr(foto, 'content_type'):
            if foto.size > 2 * 1024 * 1024:
                raise forms.ValidationError("La imagen no debe superar los 2MB.")
            
            if foto.content_type not in ['image/jpeg', 'image/png', 'image/webp']:
                raise forms.ValidationError("Formato de imagen no válido. Solo se permiten JPG, PNG o WEBP.")
        return foto

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
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['nombre']
        user.last_name = self.cleaned_data['apellido']
        user.email = self.cleaned_data['correo']
        user.username = self.cleaned_data['correo']  # Muy importante para evitar conflictos
        user.rol = self.cleaned_data['rol']
        
        if commit:
           user.save()
        return user
    
# --- Formulario para Justificativos ---

class JustificativoForm(forms.ModelForm):
    class Meta:
        model = Justificativo
        fields = ['tipo', 'fecha_ausencia', 'descripcion', 'archivo']
        widgets = {
            'tipo': forms.Select(attrs={
                'class': 'w-full p-3 mt-1 rounded-md border border-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-500 hover:bg-gray-50 text-gray-600'
            }),
            'fecha_ausencia': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full p-3 mt-1 rounded-md border border-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-500 hover:bg-gray-50 text-gray-600'
            }),
            'descripcion': forms.Textarea(attrs={
                'rows': 4,
                'class': 'w-full p-3 mt-1 rounded-md border border-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-500 hover:bg-gray-50 text-gray-600'
            }),
            'archivo': forms.ClearableFileInput(attrs={
                'class': 'w-full p-3 mt-1 rounded-md border border-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-500 hover:bg-gray-50 text-gray-600'
            }),
        }
