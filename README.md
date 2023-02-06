# Prueba R5 - Rafael Sanabria

[Aquí](https://r5-ah9a.onrender.com/docs) pueden interactuar con el modelo en producción. Se puede demorar en cargar la primera vez que se entra al link en un tiempo.

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

El desarrollo de esta sección está en el notebook `./notebooks/r5_part02_model.ipynb`. También incluye el análisis de cómo el negocio podría hacer uso de este modelo.

Para correr el notebook darle click al botón **Open in Colab** en la parte superior del mismo. No olvidar incluir la contraseña de la base de datos en la celda 4.

## Parte 3 - Scripts `./models/train.py` y `./models/predict.py`

### 3.1 Configurar el entorno

Como administrador de dependencias usé [Poetry](https://python-poetry.org/).

Para instalar los paquetes correr

```
# Con Poetry instalado
poetry install

# Con pip
pip install -r requirements.txt
```

Adicionalmente, para poder usar el script `train.py` es necesario crear el archivo `./.env` con la variable de entorno `DB_PASSWORD`.

```
DB_PASSWORD=<CONTRASEÑA QUE ESTÁ EN EL CORREO>
```

### 3.2 `./models/train.py`

Con el objetivo de que probar el modelo fuese lo más fácil posible reduje la cantidad de _features_ a 7. Así, al momento de usar la interfaz gráfica que provee FastAPI solo hay que escribir 7 valores para predecir un fraude.

El script incluye:

- Pipeline que integra en una sola clase la transformación y predicción.
- Transformación de features categóricos nominales y ordinales y numéricos discretos.
- Un `VotingClassifier` para incluir diferentes modelos de clasificación y crear un estimador más robusto.

Para mejorar los resultados se pueden incluir:

- Feature Engineering.
- Selección de features.
- Validación cruzada.
- _Hyperparameter tuning_ de los modelos.

### 3.3 `./models/predict.py`

Este script se encarga de cargar el modelo. También incluye una función que recibe un DataFrame con las features como columnas y las observaciones como filas y retorna la probabilidad de que cada observación sea un fraude.

Si se corre el comando `python ./models/predict.py` se imprimirá el resultado de una predicción de prueba para saber que el modelo está funcionando.

## Parte 4 - Despliegue en producción

### 4.1 Crear una API para consumir el modelo

La API la creé con la librería [FastAPI](https://fastapi.tiangolo.com/). El código está en el archivo `./main.py`.

Para probar la API en local es necesario correr el siguiente comando:

```bash
uvicorn main:app --reload
```

### 4.2 Subir el modelo a la nube

Después de desarrollar la API en local, usé [Render](https://render.com/) para crear un servicio en la nube. Internamente lo que hace Render es usar un contenedor de Docker con la versión de Python que uno define en la variable de entorno `PYTHON_VERSION`.

En <https://r5-ah9a.onrender.com/docs> se puede interactuar con la API.

## Cheat Sheet

```bash
# Generate Poetry requirements.txt without hashes
poetry export --without-hashes --format=requirements.txt > requirements.txt
```
