#   Program     :   p1_mlops_etl.py
#   Date        :   Febrero 13;2023
#   Author      :   Horacio Morales González
#   Sinopsis    :
#####################################################################
##Importamos las librerías
import pandas as pd
import os
from datetime import date

#Leemos todos los archivos CSV que existen en la carpeta
strCarpeta='./MLOpsReviews/'
with os.scandir(strCarpeta) as strArchivos:
    xLstArchivos = [strArchivo.name for strArchivo in strArchivos if strArchivo.is_file() and strArchivo.name.endswith('.csv')]

data_movies_final =pd.DataFrame()

for strArchivo in xLstArchivos:
    print('Leyendo archivo : '+strArchivo)
    #carga el CSV de cada platafoma
    data_platform = pd.read_csv(strCarpeta+strArchivo)
    print(data_platform.shape)
    print('Inicia transformaciones')
    #realiza las transformaciones
    #crea el campo id con la inicial de la plataforma (nombre del archivo)
    data_platform['id'] = strArchivo[0]+data_platform['show_id']
    #data_platform.set_index('id',inplace=True)
    data_platform.fillna({'rating':'G'},inplace=True)
    #limpia los espacios antes y después del dato de la columna 'date_added' porque marca error en el archivo netflix
    data_platform['date_added']=data_platform['date_added'].str.strip()
    data_platform['date_added_std'] = pd.to_datetime(data_platform['date_added'],format='%B %d, %Y')
    #continua con la transformación a minúsculas
    data_platform['type'] = data_platform['type'].str.lower()
    data_platform['title'] = data_platform['title'].str.lower()
    data_platform['director'] = data_platform['director'].str.lower()
    #coloca 'NA' en los nulos de la columna cast, porque al convertir a minúsculas me marca error en el archivo hulu
    data_platform['cast'].fillna('NA',inplace=True)
    #continúa con la transformación
    data_platform['cast'] = data_platform['cast'].str.lower()
    data_platform['country'] = data_platform['country'].str.lower()
    data_platform['date_added'] = data_platform['date_added'].str.lower()
    data_platform['rating'] = data_platform['rating'].str.lower()
    data_platform['duration'] = data_platform['duration'].str.lower()
    data_platform['listed_in'] = data_platform['listed_in'].str.lower()
    data_platform['description'] = data_platform['description'].str.lower()
    data_platform['duration_int'] = data_platform['duration'].str.split(' ').str[0]
    data_platform['duration_type'] = data_platform['duration'].str.split(' ').str[1]
    #coloca 0 donde haya nulos en la duration_int para poder pasar a minúsculas, para identificarlos después
    data_platform['duration_int'].fillna(0,inplace=True)
    #borra las columnas showid y duration, que fueron transformadas
    data_platform.drop('show_id', axis=1, inplace=True)
    data_platform.drop('duration', axis=1, inplace=True)
    data_platform.drop('date_added', axis=1, inplace=True)
    #
    print(data_platform.shape)
    #
    #concatena en el dataframe final
    data_movies_final = pd.concat([data_movies_final, data_platform], sort = False)
print('Terminó el proceso de archivos de plataformas')
print(data_movies_final.shape)

## listo el archivo de títulos, lo guardaremos al final
##ahora vamos con los archivos de ratings
#Leemos todos los archivos CSV que existen en la carpeta
strCarpetaRatings='./MLOpsReviews/ratings/'
with os.scandir(strCarpetaRatings) as strArchivos:
    xLstArchivos = [strArchivo.name for strArchivo in strArchivos if strArchivo.is_file() and strArchivo.name.endswith('.csv')]

data_ratings_final =pd.DataFrame()

for strArchivo in xLstArchivos:
    print('Leyendo archivo : '+strArchivo)
    #carga el CSV de cada platafoma
    data_ratings = pd.read_csv(strCarpetaRatings+strArchivo)
    print(data_ratings.shape)
    #realiza las transformaciones
    data_ratings['timestamp'] = data_ratings['timestamp'].apply(date.fromtimestamp)

    #concatena en el dataframe final
    data_ratings_final = pd.concat([data_ratings_final, data_ratings], sort = False)

print('terminó el proceso de archivos rating')
print(data_ratings_final.shape)

print('Obtiene el promedio por películas desde ratings y lo inserta en movies')
#Se trae el promedio de calificación de las películas de data_ratings_final y lo pega en data_movies_final
data_movies_final = pd.merge(left=data_movies_final,right=data_ratings_final.groupby(by=['movieId'])['rating'].mean().round(1), how='left', left_on='id', right_on='movieId')

#renombra la columna rating_y a: score y la original rating_x a: rating
data_movies_final.rename(columns={'rating_x':'rating'}, inplace=True)
data_movies_final.rename(columns={'rating_y':'score'}, inplace=True)


print('data_movies_final shape')
print(data_movies_final.shape)

#guarda los archivos en formato parquet
data_ratings_final.to_parquet('./datasets_parciales/ratings_final.parquet')
#table = pa.Table.from_pandas(data_movies_final)
#pq.write_table(table, 'titles_total.parquet')
data_movies_final.to_csv('./datasets_parciales/titles_total.csv')