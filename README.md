# GMXpress EVA 3

## Descripción del Proyecto

GMXpress EVA 3 es una aplicación web desarrollada con Django que permite gestionar empleados, productos, especialidades y áreas en un sistema de gestión médica. Incluye funcionalidades para crear, editar, eliminar y listar registros con validaciones específicas.

## Instalación

1. Clona el repositorio o descarga los archivos del proyecto.
2. Navega al directorio del proyecto: `cd gmxpress`
3. Instala las dependencias: `pip install -r ../requirements.txt`
4. Ejecuta las migraciones: `python manage.py migrate`
5. Crea un superusuario: `python manage.py createsuperuser`
6. Ejecuta el servidor: `python manage.py runserver`

## Credenciales de Prueba

- Usuario: 'root'
- Contraseña: ''

## Funcionalidades

- Gestión de empleados con validaciones de ID único, fechas de nacimiento entre 1960 y hoy, y nombres con letras y espacios.
- Gestión de productos con validaciones similares.
- Autenticación de usuarios.
- Interfaz web para CRUD operations.
