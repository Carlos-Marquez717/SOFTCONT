# Arquitectura

SOFTCONT se mantiene como un monolito Django modular. Esta decision evita complejidad innecesaria y permite que el proyecto crezca por areas de negocio sin cambiar la base de datos actual.

## Estructura actual

```text
SOFTCONT/
  bodega/              Configuracion principal de Django
  app/
    migrations/        Historial de base de datos
    routes/            Rutas separadas por dominio
    services/          Logica reutilizable fuera de las vistas
    static/            Archivos CSS, JS e imagenes
    templates/         Plantillas HTML
    models.py          Modelos actuales del dominio
    forms.py           Formularios Django
    views.py           Vistas existentes
```

## Dominios

Las rutas estan separadas por area funcional:

- `auth`: registro y cierre de sesion.
- `core`: home y vistas generales.
- `empresas`: empresas o grupos.
- `trabajadores`: obreros y trabajadores.
- `inventario`: materiales y herramientas.
- `pedidos`: solicitudes y reportes asociados a pedidos.
- `prestamos`: prestamos de herramientas.
- `repuestos`: repuestos y retiros.
- `utiles_aseo`: registro de utiles de aseo.
- `reportes`: PDFs, cargas y reportes especiales.

## Criterio de escalamiento

El siguiente paso recomendado no es pasar a microservicios. Para este tipo de sistema, lo mas sano es seguir como monolito modular:

1. Mover consultas repetidas a `selectors.py`.
2. Mover reglas de negocio a `services/`.
3. Mantener vistas delgadas: recibir request, validar formulario, llamar servicios y renderizar.
4. Agregar tests por dominio.
5. Solo separar modelos en apps nuevas cuando exista una migracion planificada de base de datos.

## Por que no se movieron los modelos

Los modelos siguen en `app/models.py` para no romper migraciones ni tablas existentes. En Django, mover modelos entre apps cambia el `app_label` y puede requerir migraciones manuales de contenido, permisos y tablas intermedias.

Si el proyecto crece mas, se puede planificar una segunda etapa para dividir modelos por apps reales, pero con respaldo de base de datos y migraciones controladas.
