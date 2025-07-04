# Sistema de Gestión de Asistencias OnTime

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-4.x-green?logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-blue?logo=postgresql)

Sistema desarrollado con Django que permite registrar la asistencia de aprendices por escaneo de códigos QR o ingreso manual. Pensado para instituciones educativas con roles diferenciados: administrador, instructor y aprendiz. Incluye funciones modernas como centro de ayuda, contacto, y estadísticas.

## Tecnologías utilizadas

- **Backend:** Django 4.x (Python 3.10+)
- **Base de datos:** PostgreSQL
- **Frontend:** HTML5, CSS3, Tailwind CSS, JavaScript
- **Librerías:** `html5-qrcode` para escaneo de QR, `FontAwesome`, `AOS` para animaciones
- **Otros:** DAPHNE (para ASGI), autenticación personalizada, ORM de Django

## Roles del sistema

- **Administrador:** Gestiona usuarios, clases, visualiza reportes y controla el sistema.
- **Instructor:** Registra asistencia, crea códigos QR, gestiona clases y competencias.
- **Aprendiz:** Registra asistencia escaneando o ingresando códigos y consulta su historial.

## Funcionalidades principales

- Registro de asistencia por QR o código manual
- Generación automática de códigos por clase
- Visualización de historial con filtros avanzados por fecha, estado y aprendiz
- Dashboard por rol con estadísticas y notificaciones
- Panel de administración personalizado con diseño moderno
- Contacto y Centro de ayuda (FAQs) conectados a base de datos
- Soporte para justificación de inasistencias
- Animaciones con AOS y diseño responsive para dispositivos móviles

## Requisitos

- Python 3.10 o superior
- PostgreSQL en ejecución
- Navegador moderno con soporte para cámara
- `pip` para instalar dependencias

## Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/Nicomb96/OnTime.git
cd OnTime

# 2. Crear entorno virtual
python -m venv .venv
source .venv/bin/activate      # Linux/Mac
.venv\\Scripts\\activate       # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar base de datos en settings.py o .env
# DB_NAME=postgres
# DB_USER=postgres
# DB_PASSWORD=*********
# DB_HOST=localhost
# DB_PORT=5432

# 5. Aplicar migraciones
python manage.py migrate

# 6. Crear superusuario (opcional)
python manage.py createsuperuser

# 7. Ejecutar el servidor

- Opción 1: Solo en el equipo (modo local)
python manage.py runserver

- Opción 2: Acceso desde otros dispositivos (modo red local)
daphne -b 0.0.0.0 -p 8000 ontime.asgi:application

Acceder desde otros dispositivos con la IP del equipo,
ejemplo: http://192.168.1.10:8000

Recomendaciones:
- Tener Daphne instalado: pip install daphne
- Habilitar el puerto 8000 en tu firewall si es necesario

Estructura del proyecto
ontime/
├── ontime_app/           # App principal
├── templates/            # HTML con Django Templates
├── static/               # CSS, JS, imágenes
├── manage.py             # Script de gestión Django
├── requirements.txt      # Dependencias del proyecto

Contacto

¿Dudas o soporte? Escribe al equipo desarrollador:

GitHub: Nicomb96
Correo: Ontimeproyecto1290@gmail.com

© 2025 OnTime Project. Todos los derechos reservados. Distribuido bajo licencia MIT.
