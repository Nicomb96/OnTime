from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

# --- Rutas Principales del Proyecto ---

urlpatterns = [

    path('admin/', admin.site.urls),
path('', include('ontime_app.urls')),  # ✅ Esta sí va aquí
]

# --- Servir Archivos Media en Modo Desarrollo ---

# Esta condición asegura que los archivos de medios (como fotos de perfil subidas)
# solo se sirvan directamente a través de Django cuando `settings.DEBUG` es True.
if settings.DEBUG:
    # Añade una regla de URL para servir archivos desde `settings.MEDIA_ROOT`
    # bajo la URL `settings.MEDIA_URL`.
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)