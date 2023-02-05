# Prueba R5 - Rafael Sanabria

## Parte 1 - PostgreSQL

### 1. Creación de la base de datos.

Para crear la base de datos en PostgreSQL y hostearla en la nube usé [Supabase](https://supabase.com/). Las credenciales para acceder a la base de datos son las siguientes (la contraseña está en el correo por razones de seguridad):

```json
{
  "host": "db.kowllitbpmdnyshbtbzn.supabase.co",
  "database": "postgres",
  "port": "5432",
  "user": "postgres",
  "password": "LA CONTRASEÑA ESTÁ EN EL CORREO"
}
```

### 2. Consulta de porcentaje de fraudes mensuales, semanales y diarios.

El query que produce la tabla de la prueba es

```sql
SELECT DISTINCT
  "Monthh",
  "WeekOfMonth",
  "DayOfWeek",
  ROUND(AVG("FraudFound_P") OVER (PARTITION BY "Monthh")*100, 2)::float AS percentage_fraud_month,
  ROUND(AVG("FraudFound_P") OVER (PARTITION BY "Monthh", "WeekOfMonth")*100, 2)::float AS percentage_fraud_month_week,
  ROUND(AVG("FraudFound_P") OVER (PARTITION BY "Monthh", "WeekOfMonth", "DayOfWeek")*100, 2)::float AS percentage_fraud_month_week_day
FROM public.fraudes
ORDER BY
  "Monthh" ASC,
  "WeekOfMonth" ASC
```

Para probar la consulta creé un notebook que se conecta a la base de datos que está en la nube y envía el query de SQL.

Los pasos para usarlo son:

1. Ir al notebook en `./notebooks/r5_part01_sql.ipynb`.
2. Darle click al botón al inicio del notebook que dice **Open in Colab**
3. Ingresar la clave de la base de datos. La clave está en el correo.

## Parte 2 - Análisis de datos y entrenamiento de los modelos.

### 2.1 Crear el archivo `./.env`

En este archivo agregar la contraseña de la base de datos que está en el correo.

```
DB_PASSWORD=...
```

### 2.2

### 4.

## Parte 3 - Despliegue en producción

### 3.1 Simplicar el modelo

Con el objetivo de que probar el modelo fuese lo más fácil posible reduje la cantidad de _features_ a 7. Así, al momento de usar la interfaz gráfica que provee FastAPI solo hay que escribir 7 valores para predecir un fraude.

El script `./models/train.py` se encarga de producir el modelo entrenado con las 7 features.

### 3.2 Crear una API para consumir el modelo

La API la creé con la librería [FastAPI](https://fastapi.tiangolo.com/). El código está en el archivo `./main.py`. Dentro de este archivo hago uso del script `./models/predict.py` que se encarga de cargar el modelo. También incluye una función que recibe un DataFrame con las features como columnas y las observaciones como filas y retorna la probabilidad de que cada observación sea un fraude.

Para probar la API en local es necesario correr el siguiente comando:

```bash
uvicorn main:app --reload
```

### 3.3 Subir el modelo a la nube

Después de desarrollar la API en local, usé [Render](https://render.com/) para crear un servicio en la nube. Internamente lo que hace Render es usar un contenedor de Docker con la versión de Python que uno define en la variable de entorno `PYTHON_VERSION`.

En <https://r5-ah9a.onrender.com/docs> se puede interactuar con la API.

## Cheat Sheet

```bash
# Generate Poetry requirements.txt withou hases
poetry export --without-hashes --format=requirements.txt > requirements.txt
```
