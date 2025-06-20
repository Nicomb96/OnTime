from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.forms import ModelForm
from .models import UsuarioPersonalizado, Clase

class UsuarioForm(ModelForm):
    class Meta:
        model = UsuarioPersonalizado
        fields = '__all__'

class UsuarioPersonalizadoAdmin(UserAdmin):
    model = UsuarioPersonalizado
    form = UsuarioForm

    # Usamos el método 'mostrar_clases' en vez del campo directo
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'rol',
        'mostrar_clases',
        'is_staff',
        'is_active',
    )

    list_filter = (
        'rol',
        'is_staff',
        'is_active',
    )

    search_fields = (
        'email',
        'username',
        'first_name',
        'last_name',
    )

    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Información personal', {
            'fields': ('first_name', 'last_name', 'rol', 'clases', 'foto_perfil'),
        }),
        ('Permisos', {
            'fields': (
                'is_staff',
                'is_active',
                'is_superuser',
                'groups',
                'user_permissions',
            ),
        }),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'email',
                'first_name',
                'last_name',
                'rol',
                'clases',
                'password',
                'is_staff',
                'is_active',
            ),
        }),
    )

    # Método para mostrar las clases como texto en list_display
    def mostrar_clases(self, obj):
        return ", ".join([clase.nombre for clase in obj.clases.all()])
    mostrar_clases.short_description = "Clases"

# Registrar modelos
admin.site.register(UsuarioPersonalizado, UsuarioPersonalizadoAdmin)
admin.site.register(Clase)
