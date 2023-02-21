<img src=./scr/pi1_mlops_repo_header.png>
<hr>
# sistema-de-recomendacion
Sistema de Recomendaciones de películas de las diversas plataformas de streaming. Desarrollado usando la librería surprise de sci kit_learn.
<hr>

## Rol a desarrollar

Se trata de simular una start-up que provee servicios de agregación de plataformas de streaming. Vamos a crear nuestro primer modelo de ML que soluciona un problema de negocio: un sistema de recomendación que aún no ha sido puesto en marcha! 

El dataset es complicado: Datos sin transformar, no hay procesos automatizados para la actualización de nuevas películas o series.

Se crean procesos desde cero, haciendo un trabajo rápido de **`Data Engineer`** y tener un **`MVP`** (_Minimum Viable Product_) en una semana!

<hr>

## **CONTENIDO**

**`Transformaciones`**:  Para este MVP no necesitas perfección, ¡necesitas rapidez! ⏩ Vas a hacer estas, ***y solo estas***, transformaciones a los datos:
<p> Programa :**pi1_mlops_etl.py**</p>

+ Generar campo **`id`**: Cada id se compondrá de la primera letra del nombre de la plataforma, seguido del show_id ya presente en los datasets (ejemplo para títulos de Amazon = **`as123`**)

+ Los valores nulos del campo rating deberán reemplazarse por el string “**`G`**” (corresponde al maturity rating: “general for all audiences”

+ De haber fechas, deberán tener el formato **`AAAA-mm-dd`**

+ Los campos de texto deberán estar en **minúsculas**, sin excepciones

+ El campo ***duration*** debe convertirse en dos campos: **`duration_int`** y **`duration_type`**. El primero será un integer y el segundo un string indicando la unidad de medición de duración: min (minutos) o season (temporadas)

<br/>

**`Desarrollo API`**:   Se ha creado una API usando el framework ***FastAPI***. Las consultas son las siguientes:
<P> Programa :**main.py**</P>

+ Película con mayor duración con filtros opcionales de AÑO, PLATAFORMA Y TIPO DE DURACIÓN. (la función debe llamarse get_max_duration(year, platform, duration_type))

+ Cantidad de películas por plataforma con un puntaje mayor a XX en determinado año (la función debe llamarse get_score_count(platform, scored, year))

+ Cantidad de películas por plataforma con filtro de PLATAFORMA. (La función debe llamarse get_count_platform(platform))

+ Actor que más se repite según plataforma y año. (La función debe llamarse get_actor(platform, year))

<br/>

**`Deployment`**: Se ha usado [Deta.Space] para hacer el deployment de aplicaciones:
- https://deta.space/discovery/r/nhnfiqkc64xkvifv

**`Análisis exploratorio de los datos`**: _(Exploratory Data Analysis-EDA)_
<p>Progframa : **pi1_mlops_eda.ipynb**</p>

Ya los datos están limpios, ahora es tiempo de investigar las relaciones que hay entre las variables de los datasets, ver si hay outliers o anomalías (que no tienen que ser errores necesariamente :eyes: ), y ver si hay algún patrón interesante que valga la pena explorar en un análisis posterior.

**`Sistema de recomendación`**: 
<p> Programa :**pi1_mlops.modelo.ipynb**</p>
Una vez que toda la data es consumible por la API ya lista para consumir para los departamentos de Analytics y de Machine Learning, y nuestro EDA bien realizado entendiendo bien los datos a los que tenemos acceso, es hora de entrenar nuestro modelo de machine learning para armar un sistema de recomendación de películas para usuarios, donde dado un id de usuario y una película, nos diga si la recomienda o no para dicho usuario.


**`Interfaz de consulta`**: 
<p> Se ha quedado para una segunda etapa la consulta de predicciones mediante un bot de telegram, incluyo el script hasta donde voy en este momento. 
Programa : **pi1_mlops_bot.py**
<br>

<hr>

**`Consideraciones finales`**
<p>
El dataset  original se encuentra en :

<p>https://drive.google.com/drive/folders/1rDKXH4yUdLJQ1SMHAXPssDFLVSCMTY1p?usp=sharing

<p> los archivos de carga para el módulo etl se cargan en la carpeta MLOpsReviews, y posterior a la transformación se cargan en la carpeta **datasets_parciales** desde donde se consumen por los demás módulos
