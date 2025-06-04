from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Rutas principales del proyecto
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ontime_app.urls')),
]

# Servir archivos media en modo debug
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)