#   Program     :   p1_mlops_api.py
#   Date        :   February 13th;2023
#   Author      :   Horacio Morales González
#   Sinopsis    :   Create an API in order to consume data from movies dataset
##############################################################################
##Importamos las librerías
import pandas as pd
from collections import Counter

def get_max_duration(year: int = 0 , platform = '', duration_type: int = 0):
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

def get_score_count(platform, score, year):
    '''
    Cantidad de películas por plataforma con un puntaje mayor a XX en determinado año 
    (la función debe llamarse get_score_count(platform, scored, year))
    los parámetros son opcionales
    '''
    intNumPeliPuntaje = int(data_movies.query("id.str.startswith(@platform[0]) and score >= @score and release_year == @year")['id'].count())
    return intNumPeliPuntaje

def get_count_platform(platform):
    '''
    Cantidad de películas por plataforma con filtro de PLATAFORMA. 
    (La función debe llamarse get_count_platform(platform))
    el parámetro es obligatorio
    '''
    intNumPeliculas = int(data_movies[data_movies['id'].str.startswith(platform[0])]['id'].count())
    return intNumPeliculas

def get_actor(platform, year):
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

def get_title(movieId):
    '''
    devuelve el título de la película, apartir del id recibido

    '''
    titulo=str(data_movies[(data_movies['id']==movieId)].title)
    return titulo

def get_movies(usuarioId,score):
    data_usuario = data_ratings[(data_ratings['userId'] == usuarioId) & (data_ratings['rating']>=score)][['movieId','rating']]
    data_usuario = pd.merge(left=data_usuario,right=data_movies[['id','title']], how='left', left_on=data_usuario.movieId, right_on='id')
    data_usuario.drop('id',axis=1)
    return data_usuario


#Módulo principal del programa
if __name__ == '__main__':
    
    #cargamos los dataframe para ser usados en los métodos arriba definidos
    data_movies = pd.read_csv('./MLOpsReviews/titles_total.csv')
    data_ratings = pd.read_csv('./MLOpsReviews/ratings/ratings_final.csv')
    
    #invocamos los métodos definidos
    #print('sin parametros')
    #print(get_max_duration())
    #print('con parametros')
    #print(get_max_duration(year=2017))
    #print('la película del id ns8168 es :',get_title('ns8168'))
    #print('la película del usuario 3978	son :')
    #print(get_movies(3978,3.0))