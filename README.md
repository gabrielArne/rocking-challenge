# Rocking Challenge

Este repositorio contiene los scripts necesarios para descargar los catálogos de Disney+ y Netflix, normalizar la información y poblarla en PostgreSQL (o recrear el esquema vía SQL). A continuación se detallan los pasos para preparar el entorno, obtener los datos y trabajar con la base. En el mail de entrega se adjuntan credenciales de acceso a instancia de postgreSQL en Supabase.

## 1. Crear y activar el entorno virtual

# Desde la raíz del proyecto
python -m venv .venv

### Instalar dependencias

Con el entorno activo:

pip install -r requirements.txt
```

## 2. Descargar los CSV originales y correr el jupyter notebook de EDA

Las URLs oficiales están definidas en `.env` (`DISNEY_URL`, `NETFLIX_URL`). El script `functions/get_by_url.py` expone la función `download_csv_from_url` que puedes invocar desde la línea de comandos. 

Corre el jupyter notebook `eda.ipynb` para explorar los datos, hacer limpieza y combinar ambos datasets en un solo CSV (`data/combined_streaming_data.csv`).

## 3. Crear el esquema de base de datos

El módulo `db/init_db.py` crea todas las tablas normalizadas leyendo la cadena `DB_URI` del `.env`.

## 4. Poblar las tablas con el CSV combinado

python -m db.populate_db

El script reutiliza las dimensiones existentes y sólo inserta las películas que falten, construyendo las relaciones N:N (actores, directores, países y categorías).

## 5. Consultas y stored procedure

- **Consultas de desafío**: `db/queries/desafio/*.sql` incluye
  - `actor_mas_peliculas.sql`: Actor con más apariciones en Netflix.
  - `top10_actores_anio_act.sql`: Top 10 de actores del año en curso (Netflix + Disney+).
- **Stored Procedure**: `db/queries/stored_procedures/sp_get_top5_pelis_largas.sql` define un procedimiento PL/pgSQL que retorna las 5 películas más largas (en minutos) para un año dado usando un cursor.

## 6. Esquema de la base

![Esquema de la base](utils/supabase-schema-svijsdurswxeyifewhrn.png)

La imagen resume la tercera forma normal implementada: `movies` como tabla central con dimensiones (`content_types`, `ratings`, `duration_types`, `platforms`) y tablas intermedias para directores, actores, países y categorías.

