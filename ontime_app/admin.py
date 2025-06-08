from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.forms import ModelForm
from .models import UsuarioPersonalizado

# --- Formulario para el Modelo de Usuario Personalizado en el Admin ---

class UsuarioForm(ModelForm):
    """
    Define el formulario que el administrador usará para crear o editar
    instancias de UsuarioPersonalizado en el panel de administración.
    """
    class Meta:
        """
        Clase Meta para configurar el formulario.
        """
        model = UsuarioPersonalizado  # Asocia este formulario al modelo UsuarioPersonalizado
        fields = '__all__'  # Incluye todos los campos del modelo en el formulario

# --- Configuración del Panel de Administración para UsuarioPersonalizado ---

class UsuarioPersonalizadoAdmin(UserAdmin):
    """
    Personaliza cómo se muestra y se gestiona el modelo UsuarioPersonalizado
    en el panel de administración de Django. Extiende UserAdmin para mantener
    la funcionalidad base de gestión de usuarios.
    """
    model = UsuarioPersonalizado  # Asocia esta configuración de admin con el modelo personalizado
    form = UsuarioForm  # Usa el formulario UsuarioForm para la creación/edición de usuarios

    # Define las columnas que se mostrarán en la lista de usuarios en el admin
    list_display = (
        'username',    # Nombre de usuario
        'email',       # Correo electrónico
        'first_name',  # Primer nombre
        'last_name',   # Apellido
        'rol',         # Rol del usuario (aprendiz, instructor, admin)
        'is_staff',    # Si tiene acceso al panel de administración
        'is_active',   # Si la cuenta está activa
    )

    # Define los campos por los que se puede filtrar la lista de usuarios
    list_filter = (
        'rol',         # Filtrar por rol
        'is_staff',    # Filtrar por personal del staff
        'is_active',   # Filtrar por estado activo
    )

    # Define los campos por los que se puede buscar usuarios
    search_fields = (
        'email',       # Buscar por correo electrónico
        'username',    # Buscar por nombre de usuario
        'first_name',  # Buscar por primer nombre
        'last_name',   # Buscar por apellido
    )

    # Define el orden predeterminado de los usuarios en la lista
    ordering = ('email',)

    # Organiza los campos en secciones dentro del formulario de edición de usuario
    fieldsets = (
        (None, {  # Primera sección sin título explícito
            'fields': ('username', 'email', 'password'),  # Campos básicos de autenticación
        }),
        ('Información personal', {  # Sección para datos personales
            'fields': ('first_name', 'last_name', 'rol', 'foto_perfil'),  # Nombre, apellido, rol y foto
        }),
        ('Permisos', {  # Sección para gestionar permisos y grupos
            'fields': (
                'is_staff',         # Acceso al admin
                'is_active',        # Cuenta activa
                'is_superuser',     # Superusuario
                'groups',           # Grupos de usuarios
                'user_permissions', # Permisos individuales
            ),
        }),
        ('Fechas importantes', {  # Sección para fechas de registro y último login
            'fields': ('last_login', 'date_joined'), # Último login y fecha de creación de cuenta
        }),
    )

    # Define los campos que se mostrarán en el formulario para añadir un nuevo usuario
    add_fieldsets = (
        (None, {  # Sección sin título
            'classes': ('wide',),  # Clase CSS para ocupar todo el ancho disponible
            'fields': (
                'username',
                'email',
                'first_name',
                'last_name',
                'rol',
                'password',  # Contraseña inicial
                'is_staff',
                'is_active',
            ),
        }),
    )

# Registra el modelo UsuarioPersonalizado en el panel de administración
# con la configuración personalizada definida en UsuarioPersonalizadoAdmin.
admin.site.register(UsuarioPersonalizado, UsuarioPersonalizadoAdmin)