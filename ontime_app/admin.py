from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UsuarioPersonalizado
from django.forms import ModelForm

class UsuarioForm(ModelForm):
    class Meta:
        model = UsuarioPersonalizado
        fields = '__all__'

class UsuarioPersonalizadoAdmin(UserAdmin):
    model = UsuarioPersonalizado
    form = UsuarioForm
    list_display = ('username', 'email', 'first_name', 'last_name', 'rol', 'is_staff', 'is_active')
    list_filter = ('rol', 'is_staff', 'is_active')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Información personal', {'fields': ('first_name', 'last_name', 'rol')}),
        ('Permisos', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas importantes', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'rol', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

admin.site.register(UsuarioPersonalizado, UsuarioPersonalizadoAdmin)
