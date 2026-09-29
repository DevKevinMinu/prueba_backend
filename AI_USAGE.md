# AI_USAGE.md

## Herramienta utilizada

Se utilizó ChatGPT como herramienta de apoyo durante el desarrollo
de la prueba técnica.

La IA se utilizó como apoyo para comprender conceptos, analizar
problemas, revisar código y proponer posibles soluciones.

La implementación final fue revisada y validada manualmente.

## 1. Configuración inicial del proyecto

### Problema consultado

Se solicitó orientación para estructurar una API REST utilizando
Django REST Framework, PostgreSQL y Docker Compose.

### Uso de IA

Se consultaron aspectos relacionados con:

- Estructura del proyecto Django.
- Configuración de Django REST Framework.
- Modelos Patient y Treatment.
- Configuración de PostgreSQL.
- Docker Compose.
- Variables de entorno.

### Cambios realizados

Las propuestas fueron adaptadas al proyecto y posteriormente
probadas mediante Docker y las migraciones de Django.

### Verificación

Se verificó que:

- El proyecto iniciara correctamente.
- PostgreSQL estuviera disponible.
- Las migraciones se ejecutaran correctamente.
- La API respondiera correctamente.

## 2. Validaciones y serializers

### Problema consultado

Se solicitó ayuda para implementar validaciones en Django REST
Framework.

Entre ellas:

- Fecha de nacimiento no futura.
- Fecha de finalización de tratamiento posterior o igual a la
  fecha de inicio.
- Identificación compuesta únicamente por números.

### Propuesta generada

Se propusieron validaciones mediante métodos de los serializers,
como:

```python
validate_birth_date()
validate_identification()
validate()
```

### Cambios realizados

Las validaciones fueron incorporadas al proyecto y adaptadas a los
modelos y serializers existentes.

### Verificación

Se verificó el comportamiento mediante pruebas automatizadas y
solicitudes a la API.

## 3. Tratamientos activos

### Problema consultado

Inicialmente el endpoint de tratamientos activos devolvía solamente
el primer tratamiento activo de un paciente.

Se consultó cómo modificarlo para devolver todos los tratamientos
activos.

### Propuesta generada

Se propuso eliminar el uso de `.first()` y serializar la colección
utilizando:

```python
TreatmentSerializer(
    treatments,
    many=True
)
```

### Cambios realizados

El endpoint fue modificado para devolver una lista de tratamientos
activos.

La respuesta también contempla el caso en el que el paciente no
tiene tratamientos activos:

```json
{
    "has_active_treatment": false,
    "treatments": []
}
```

### Verificación

Se agregó/modificó una prueba automatizada para comprobar que un
paciente con múltiples tratamientos activos reciba todos los
tratamientos correspondientes.

## 4. Análisis del problema N+1

### Problema consultado

La prueba técnica proporciona un fragmento de código que consulta
los tratamientos dentro de un ciclo de pacientes.

El problema consultado fue identificar:

- N+1 queries.
- Paginación.
- Serialización.
- Performance.
- Seguridad.
- Escalabilidad.

### Propuesta analizada

Se identificó que realizar:

```python
Treatment.objects.filter(patient=patient)
```

dentro de un ciclo puede generar una consulta adicional por cada
paciente.

Se analizó el uso de:

```python
prefetch_related()
```

para optimizar relaciones de tipo uno a muchos.

También se analizó la necesidad de paginación y serializers.

### Verificación

El problema fue analizado conceptualmente y comparado con el
funcionamiento del ORM de Django.

No se incorporó este código de ejemplo directamente al endpoint
principal del proyecto, ya que corresponde al ejercicio de debugging
proporcionado por la prueba.

## 5. Testing

### Problema consultado

Se solicitó apoyo para identificar qué escenarios debían probarse en
la API.

### Cambios realizados

Se crearon pruebas para:

- Creación de pacientes.
- Consulta de pacientes.
- Actualización mediante PATCH.
- Validación de fecha de nacimiento.
- Recursos inexistentes.
- Creación de tratamientos.
- Actualización de tratamientos.
- Validación de fechas.
- Tratamientos activos.
- Restricción del método PUT.

### Verificación

Las pruebas fueron ejecutadas mediante:

```bash
docker compose exec backend python manage.py test
```

El resultado fue utilizado para verificar que los cambios no
introdujeran regresiones.

## 6. SQL

### Problema consultado

Se solicitó orientación para construir las consultas SQL requeridas
por la prueba.

### Consultas desarrolladas

Se trabajaron consultas para:

1. Pacientes con tratamientos activos.
2. Pacientes sin tratamientos.
3. Cantidad de tratamientos por paciente.
4. Tratamiento más reciente por paciente.
5. Top 10 pacientes por cantidad de tratamientos.

### Verificación

Las consultas fueron ejecutadas directamente sobre PostgreSQL
utilizando `psql`.

## 7. Criterio de uso de IA

La IA fue utilizada como herramienta de apoyo y no como sustituto de
la comprensión del código.

Las propuestas generadas fueron revisadas, adaptadas al proyecto y
verificadas mediante:

- Ejecución de la aplicación.
- Docker Compose.
- Migraciones.
- Consultas PostgreSQL.
- Pruebas automatizadas.
- Pruebas manuales de los endpoints.

El código final presentado en el repositorio corresponde a la versión
revisada y validada durante el desarrollo de la prueba.