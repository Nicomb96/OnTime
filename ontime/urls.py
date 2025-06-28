from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ontime_app.urls')),
]

# --- Servir Archivos Estáticos y Media en Modo Desarrollo ---
if settings.DEBUG:
    # Archivos de usuario (ej. fotos de perfil)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # Archivos estáticos (como el CSS del admin de Django)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
