# API de Pacientes y Tratamientos

API REST desarrollada con Python, Django REST Framework y PostgreSQL
para la administración de pacientes y sus tratamientos.

El proyecto fue desarrollado como parte de una prueba técnica Backend
Junior / Semi-Junior.

## Tecnologías

- Python
- Django
- Django REST Framework
- PostgreSQL
- Docker
- Docker Compose
- Git

## Arquitectura

El proyecto está organizado de la siguiente manera:

```text
prueba_backend/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── patients/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
│
├── sql/
│   └── queries.sql
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── manage.py
├── .env.example
├── .gitignore
├── README.md
└── AI_USAGE.md
```

### Entidades principales

#### Patient

Representa un paciente y contiene:

- `id`
- `identification`
- `first_name`
- `last_name`
- `birth_date`
- `created_at`

La identificación debe contener únicamente números.

#### Treatment

Representa un tratamiento asociado a un paciente y contiene:

- `id`
- `patient`
- `name`
- `start_date`
- `end_date`
- `status`
- `created_at`

Existe una relación `ForeignKey` entre `Treatment` y `Patient`.

## Requisitos

Para ejecutar el proyecto se necesita:

- Docker Desktop
- Docker Compose
- Git

No es necesario instalar PostgreSQL directamente en el equipo,
ya que PostgreSQL se ejecuta mediante Docker Compose.

## Variables de entorno

Crear un archivo `.env` en la raíz del proyecto tomando como referencia:

```text
.env.example
```

El archivo `.env` contiene las variables necesarias para la conexión
de Django con PostgreSQL.

Por seguridad, `.env` no debe subirse al repositorio.

## Ejecución con Docker

Desde la carpeta raíz del proyecto:

```bash
docker compose up --build
```

Una vez iniciados los servicios, la API estará disponible en:

```text
http://127.0.0.1:8000/
```

Para detener los servicios:

```bash
docker compose down
```

## Migraciones

Las migraciones pueden ejecutarse dentro del contenedor backend:

```bash
docker compose exec backend python manage.py migrate
```

Para comprobar el estado de las migraciones:

```bash
docker compose exec backend python manage.py showmigrations
```

## Tests

Para ejecutar las pruebas automatizadas:

```bash
docker compose exec backend python manage.py test
```

Las pruebas cubren, entre otros:

- Creación de pacientes.
- Consulta de pacientes.
- Actualización mediante `PATCH`.
- Validación de fecha de nacimiento.
- Validación de identificación numérica.
- Recursos inexistentes.
- Creación de tratamientos.
- Actualización de tratamientos.
- Validación de fechas de tratamientos.
- Consulta de tratamientos activos.
- Múltiples tratamientos activos.
- Restricción del método `PUT`.

## Endpoints

### Patients

#### Crear paciente

```http
POST /api/patients/
```

Ejemplo:

```json
{
    "identification": "10000001",
    "first_name": "Juan",
    "last_name": "Gomez",
    "birth_date": "1998-05-20"
}
```

#### Listar pacientes

```http
GET /api/patients/
```

#### Consultar paciente

```http
GET /api/patients/{id}/
```

#### Actualizar parcialmente un paciente

```http
PATCH /api/patients/{id}/
```

### Filtros

La API permite filtrar pacientes por:

```text
identification
last_name
```

Ejemplos:

```text
GET /api/patients/?identification=10000001
```

```text
GET /api/patients/?last_name=Gomez
```

### Treatments

#### Crear tratamiento

```http
POST /api/treatments/
```

Ejemplo:

```json
{
    "patient": 1,
    "name": "Fisioterapia",
    "start_date": "2026-09-21",
    "end_date": null,
    "status": "active"
}
```

#### Listar tratamientos

```http
GET /api/treatments/
```

#### Consultar tratamiento

```http
GET /api/treatments/{id}/
```

#### Actualizar parcialmente un tratamiento

```http
PATCH /api/treatments/{id}/
```

### Tratamientos activos de un paciente

```http
GET /api/patients/{id}/active-treatment/
```

Este endpoint devuelve todos los tratamientos que actualmente tienen
estado `active` para el paciente.

Ejemplo:

```json
{
    "has_active_treatment": true,
    "treatments": [
        {
            "id": 1,
            "patient": 1,
            "name": "Fisioterapia",
            "start_date": "2026-09-21",
            "end_date": null,
            "status": "active",
            "created_at": "2026-09-21T10:00:00Z"
        }
    ]
}
```

Si no existen tratamientos activos:

```json
{
    "has_active_treatment": false,
    "treatments": []
}
```

## Validaciones

La API implementa las siguientes validaciones:

- La identificación solamente puede contener números.
- La fecha de nacimiento no puede ser futura.
- La fecha de finalización de un tratamiento no puede ser anterior
  a la fecha de inicio.
- Los campos `id` y `created_at` son de solo lectura.

Los errores de validación son respondidos mediante `400 Bad Request`.

## Métodos HTTP

La API utiliza:

- `GET` para consultas.
- `POST` para creación.
- `PATCH` para actualizaciones parciales.

El método `PUT` no está habilitado para los recursos principales,
de acuerdo con el contrato definido para la prueba técnica.

## SQL

Las consultas SQL requeridas se encuentran en:

```text
sql/queries.sql
```

Incluyen:

1. Pacientes con al menos un tratamiento activo.
2. Pacientes que nunca han tenido tratamientos.
3. Cantidad de tratamientos por paciente.
4. Tratamiento más reciente de cada paciente.
5. Los 10 pacientes con mayor cantidad de tratamientos.

Las consultas utilizan JOIN, GROUP BY, agregaciones y CTE/window
functions cuando resulta conveniente.

## Debugging y N+1 Queries

La prueba técnica incluye un fragmento de código con un posible
problema de N+1 queries.

El problema aparece cuando se realiza una consulta de tratamientos
dentro de un ciclo que recorre pacientes.

La solución propuesta consiste en utilizar `prefetch_related()` para
optimizar la consulta de relaciones de tipo uno a muchos, además de
implementar paginación y serializers para controlar la cantidad y
estructura de los datos.

## Decisiones técnicas

### Django REST Framework

Se utilizaron `ModelSerializer` y `ViewSet` para separar la lógica
de serialización de la lógica de los endpoints.

### Validaciones

Las validaciones relacionadas con los datos recibidos por la API se
implementaron principalmente en los serializers.

### PATCH

Se utiliza `PATCH` porque las actualizaciones requeridas son parciales.

### PostgreSQL

PostgreSQL se utiliza como base de datos principal y se ejecuta dentro
de Docker para facilitar la reproducción del entorno.

### Docker Compose

Docker Compose permite ejecutar el backend y PostgreSQL como servicios
separados y reproducibles.

### Testing

Se utilizaron pruebas automatizadas con Django REST Framework para
verificar el comportamiento esperado de los endpoints y las
validaciones.

## Inteligencia Artificial

Durante el desarrollo se utilizó Inteligencia Artificial como
herramienta de apoyo para analizar problemas, revisar código,
comprender conceptos y proponer soluciones.

El detalle del uso de IA se encuentra en:

```text
AI_USAGE.md
```

La implementación final fue revisada y probada mediante pruebas
automatizadas y ejecución del proyecto con Docker.

## Estado del proyecto

Proyecto funcional con:

- API REST.
- PostgreSQL.
- Docker Compose.
- Validaciones.
- Paginación.
- Filtros.
- Pruebas automatizadas.
- Consultas SQL.
- Documentación.