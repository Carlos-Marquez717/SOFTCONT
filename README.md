# SOFTCONT

SOFTCONT es una aplicacion web desarrollada con Django para gestionar solicitudes, prestamos de herramientas, retiros de repuestos, utiles de aseo y reportes PDF en un entorno de bodega o faena.

## Funcionalidades principales

- Registro y listado de empresas, trabajadores, materiales, herramientas y repuestos.
- Gestion de pedidos por trabajador.
- Gestion de prestamos de herramientas.
- Control de retiro de repuestos.
- Registro de utiles de aseo por mes.
- Carga de datos desde archivos.
- Generacion de reportes PDF.
- Panel administrativo personalizado con Jazzmin.

## Tecnologias

- Python 3.11
- Django 5
- PostgreSQL en produccion
- SQLite para desarrollo local
- WhiteNoise para archivos estaticos
- Gunicorn para despliegue
- Railway como plataforma de despliegue

## Arquitectura

El proyecto esta organizado como un monolito Django modular. Las rutas se separan por dominio dentro de `app/routes/` y la logica reutilizable comienza a vivir en `app/services/`.

Para mas detalle, revisa `ARCHITECTURE.md`.

## Capturas

### Inicio de sesion

![Inicio de sesion](docs/screenshots/01-login.png)

### Panel principal

![Panel principal](docs/screenshots/02-home.png)

### Registro de pedidos

![Registro de pedidos](docs/screenshots/03-registro-pedidos.png)

### Listado y reportes de pedidos

![Listado de pedidos](docs/screenshots/04-listado-pedidos.png)

### Prestamo de herramientas

![Prestamo de herramientas](docs/screenshots/05-prestamos.png)

### Retiro de repuestos

![Retiro de repuestos](docs/screenshots/06-retiro-repuestos.png)

### Utiles de aseo

![Utiles de aseo](docs/screenshots/07-utiles-aseo.png)

### Repuestos

![Repuestos](docs/screenshots/08-repuestos.png)

## Instalacion local

1. Crear y activar un entorno virtual.

```bash
python -m venv env
env\Scripts\activate
```

2. Instalar dependencias.

```bash
pip install -r requirements.txt
```

3. Crear el archivo de entorno.

```bash
copy .env.example .env
```

4. Aplicar migraciones.

```bash
python manage.py migrate
```

5. Crear un usuario administrador.

```bash
python manage.py createsuperuser
```

6. Levantar el servidor local.

```bash
python manage.py runserver
```

## Variables de entorno

El proyecto lee la configuracion desde `.env`. Para publicar el repositorio, no subas el archivo `.env` real.

- `SECRET_KEY`: clave secreta de Django.
- `DEBUG`: `True` en local, `False` en produccion.
- `ALLOWED_HOSTS`: dominios permitidos separados por coma.
- `CSRF_TRUSTED_ORIGINS`: origenes seguros separados por coma.
- `DATABASE_URL`: cadena de conexion de PostgreSQL para produccion.

## Despliegue

El proyecto incluye `railway.json` para Railway. El comando de inicio ejecuta migraciones, recolecta archivos estaticos y levanta Gunicorn.

Antes de publicar:

- Configurar las variables de entorno en Railway.
- Usar `DEBUG=False`.
- Configurar `ALLOWED_HOSTS` con el dominio real.
- No incluir `.env`, `db.sqlite3`, `env/` ni `staticfiles/` en el repositorio.

## Nota para repositorio publico

Este repositorio esta preparado para ser mostrado como proyecto de porfolio. Si anteriormente se subieron secretos o una base de datos al historial de Git, se deben rotar esas credenciales y limpiar el historial antes de hacerlo publico.
