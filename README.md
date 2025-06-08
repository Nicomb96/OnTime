
# OnTime - Sistema de Registro de Asistencia con QR

## Descripción

Sistema desarrollado con Django que permite registrar la asistencia de aprendices a través del escaneo de códigos QR o ingreso manual de códigos generados por instructores. Está pensada para instituciones educativas y cuenta con roles diferenciados para administradores, instructores y aprendices.

---

## Tecnologías usadas

- Python 3.x  
- Django  
- PostgreSQL  
- HTML5, CSS3 y JavaScript  
- Tailwind CSS para estilos  
- Librería **html5-qrcode** para lectura de QR en el navegador  
- FontAwesome para íconos  

---

## Roles del sistema

- **Administrador:** Gestiona cuentas, usuarios y supervisa el sistema.  
- **Instructor:** Genera códigos QR y códigos alfanuméricos para registrar asistencia.  
- **Aprendiz:** Escanea los códigos para registrar su asistencia o ingresa el código manualmente si no puede escanear.

---

## Funcionalidades principales

- Registro de asistencia mediante escaneo de QR o ingreso manual de código.  
- Visualización y filtrado de historial de asistencia.  
- Generación de códigos QR y alternativos por parte del instructor.  
- Notificaciones para el usuario sobre el estado de registro.  
- Interfaz moderna y responsiva con animaciones y mensajes claros.  

---

## Requisitos

- Python 3 o superior
- PostgreSQL (configurado y corriendo)  
- Pip (para instalar dependencias)  
- Navegador web moderno con cámara para escaneo QR (opcional)

---

## Instalación y configuración

1. **Clonar el repositorio**

   - git clone https://github.com/Nicomb96/OnTime.git

2. **Crear y activar entorno virtual**

   - python -m venv .venv
   - .venv\Scripts\activate     # Windows
   
4. **Instalar dependencias**

   - pip install -r requirements.txt
   
5. **Configurar la base de datos PostgreSQL**

   - Crear base de datos y usuario PostgreSQL:
     - Base de datos: postgres
     - Usuario: postgres
     - Contraseña: nicolasmb321

   - Ajustar configuración en settings.py si se cambia datos:
   
     - DATABASES:
        - ENGINE: django.db.backends.postgresql
        - NAME: postgres                       
        - USER: postgres                        
        - PASSWORD: nicolasmb321                 
        - HOST: localhost                        
        - PORT: 5432

6. **Aplicar migraciones**

   - python manage.py migrate

     Nota: Inicialmente se consideró usar un archivo `.sql` para definir las tablas de la base de datos, no obstante se optó por utilizar el enfoque nativo de Django mediante `models.py` y migraciones. Ya que permite una mejor integración con el framework, facilita la gestión de cambios en el modelo de datos y reduce errores al evitar definiciones manuales de SQL.

7. **Crear superusuario administrador**

   El proyecto ya cuenta con el siguiente superusuario principal para pruebas:
    - Email: Ontimeproyecto1290@gmail.com
    - Contraseña: ontime654321

8. **Ejecutar el servidor de desarrollo**

   - python manage.py runserver

9. **Abrir en el navegador**

   - Accede a http://127.0.0.1:8000 y comienza a usarlo.

**Uso básico**

   - Inicia sesión con el usuario administrador para gestionar el sistema.
   - Los instructores pueden generar códigos QR desde su panel.
   - Los aprendices registran asistencia escaneando el QR con su cámara o ingresando manualmente el código.
   - La app mostrará mensajes de éxito o error al registrar asistencia.
   - Puedes consultar el historial y filtrar por fechas en la sección correspondiente.

**Estructura del proyecto**

   - ontime_app/ → Código principal de la app Django.
   - templates/ → Archivos HTML con Django Templates.
   - static/ → Archivos estáticos (CSS, JS, imágenes).
   - requirements.txt → Dependencias del proyecto.
   - manage.py → Script principal para gestión Django.

**Dependencias importantes**

   - Django
   - psycopg2-binary (para PostgreSQL)
   - html5-qrcode (librería JS cargada desde CDN)
   - Tailwind CSS (integrado para estilos)

**Contacto**

   Para dudas o soporte, contacta al grupo desarrollador:
   - GitHub: https://github.com/Nicomb96
   - Email: Ontimeproyecto1290@gmail.com
