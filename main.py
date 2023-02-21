#   Program     :   p1_mlops_api.py
#   Date        :   February 13th;2023
#   Author      :   Horacio Morales González
#   Sinopsis    :   Create an API in order to consume data from movies dataset
##############################################################################
##Importamos las librerías
import pandas as pd
from fastapi import FastAPI
from fastapi.responses import FileResponse
from collections import Counter

#cargamos los dataframe para ser usados en los métodos arriba definidos, se usan en todos los módulos
data_movies = pd.read_csv('./datasets_parciales/titles_total.csv')

app = FastAPI()

@app.get("/get_max_duration/")
def get_max_duration(year : int = 0 , platform : str = '', duration_type : str = ''):
    '''
    Película con mayor duración con filtros opcionales de AÑO, PLATAFORMA Y TIPO DE DURACIÓN.
    (la función debe llamarse get_max_duration(year, platform, duration_type))
    '''
    #la idea es hacer una sola consulta y no andar preguntando por los parámetros si vienen o no con dato
    #valores diferentes para release_year|platform|duration_type
    lstAños = data_movies['release_year'].unique().tolist()
    lstPlatform = ['a','d','h','n']
    lstDurationType = data_movies['duration_type'].unique().tolist()

    #ajusta el array, por si alguno de los parámetros viene vacío (al ser opcional es posible)
    if year == 0:
        lstAños=[]
    else:
        lstAños.remove(year)

    if platform == '':
        lstPlatform = []
    else:
        lstPlatform.remove(platform[0])

    if duration_type == 0:
        lstDurationType = []
    else:
        lstDurationType.remove(duration_type)

    #Realiza la consulta, se elije esta forma para evitar hacer comparaciones si los parámetros
    #traen o no datos, es una sola consulta para todos
    strPeliculaMaxSuration = str(data_movies[(~data_movies['release_year'].isin(lstAños)) & (~data_movies['duration_type'].isin(lstDurationType)) & (~data_movies['id'].str.startswith(tuple(lstPlatform)))].sort_values('duration_int',ascending=False).head(1)['title'])

    return strPeliculaMaxSuration

@app.get('/get_score_count/')
def get_score_count(platform : str, score : float, year : int):
    '''
    Cantidad de películas por plataforma con un puntaje mayor a XX en determinado año 
    (la función debe llamarse get_score_count(platform, scored, year))
    los parámetros son opcionales
    '''
    intNumPeliPuntaje = int(data_movies.query("id.str.startswith(@platform[0]) and score >= @score and release_year == @year")['id'].count())
    return intNumPeliPuntaje

@app.get('/get_count_platform/')
def get_count_platform(platform : str):
    '''
    Cantidad de películas por plataforma con filtro de PLATAFORMA. 
    (La función debe llamarse get_count_platform(platform))
    el parámetro es obligatorio
    '''
    intNumPeliculas = int(data_movies[data_movies['id'].str.startswith(platform[0])]['id'].count())
    return intNumPeliculas

@app.get('/get_actor/')
def get_actor(platform : str, year : int):
    '''
    Actor que más se repite según plataforma y año. 
    (La función debe llamarse get_actor(platform, year))
    los parámetros son obligatorios
    '''
    #extraemos los actores a una sola lista
    arrActores = data_movies.query("id.str.startswith(@platform[0]) and release_year == @year")['cast'].str.split(',',expand=True).to_numpy().flatten()
    #eliminamos los nulos
    arrActores = [item for item in arrActores if (item and item != 'na')]
    #eliminamos  los 'na'
    return Counter(arrActores).most_common()[0][0]

@app.get('/get_title/')
def get_title(movieId: str):
    '''
    devuelve el título de la película, apartir del id recibido

    '''
    titulo=str(data_movies[(data_movies['id']==movieId)].title)
    return titulo

@app.get('/get_movies')
def get_movies(usuarioId: int,score: float):
    '''
    Devuelve todas las películas que el usuario ha calificado
    '''
    #se carga el archivo de ratings aquí, porque solo se ocupa en este módulo
    data_ratings = pd.read_parquet('./datasets_parciales/ratings_final.parquet')

    data_usuario = data_ratings[(data_ratings['userId'] == usuarioId) & (data_ratings['rating']>=score)][['movieId','rating']]
    data_usuario = pd.merge(left=data_usuario,right=data_movies[['id','title']], how='left', left_on=data_usuario.movieId, right_on='id')
    data_usuario.drop('id',axis=1)
    return data_usuario

