# importa las librerias necesarias
from fastapi import FastAPI
import pandas as pd
import pickle
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

# carga la base de datos contenia de el archivo picke
df_movie = pd.read_pickle('./Data/api.pickle')

# Crea una instamcia de la clase FASTAPI
app = FastAPI()

# Decorador en el framework FastAPI que define una ruta para una solicitud HTTP GET
@app.get('/cantidad_filmaciones_mes/{mes}')
# Esta funcion tiene como parametro un mes del año y retorna un diccionario con mes y cantidad de peliculas estrenadas ese mismo mes
def cantidad_filmaciones_mes(mes:str):
    months = {
        "enero": 1,
        "febrero": 2,
        "marzo": 3,
        "abril": 4,
        "mayo": 5,
        "junio": 6,
        "julio": 7,
        "agosto": 8,
        "septiembre": 9,
        "octubre": 10,
        "noviembre": 11,
        "diciembre": 12
    }

    if not isinstance(mes, str):
        return 'Debe ingresar un texto, por ejemplo, por ejemplo: enero'
    elif mes.lower() not in months:
        return 'Debe ingresar un mes válido del año, por ejemplo: enero'
    else:
        mes = mes.lower()
        month = months[mes]
        resp = df_movie[(df_movie['release_month'] == month)]['release_month'].count()
        return {'mes': mes, 'cantidad': str(resp)}




@app.get('/cantidad_filmaciones_dia{dia}')
# Esta funcion tiene como parametro un dia de la semana y retorna un diccionario con dia y cantidad de peliculas estrenadas ese mismo dia
def cantidad_filmaciones_dia(dia:str):
    days = {
    'lunes': 'Monday',
    'martes': 'Tuesday',
    'miércoles': 'Wednesday',
    'jueves': 'Thursday',
    'viernes': 'Friday',
    'sábado': 'Saturday',
    'domingo': 'Sunday'}

    if not isinstance(dia, str):
        return 'Debe ingresar un texto, por ejemplo: sabado'
    elif dia.lower() not in days:
        return 'Debe ingresar un dia de la semana, por ejemplo: sabado'
    else:
        dia = dia.lower()
        day = days[dia]
        resp = df_movie[(df_movie['release_day'] == day)]['release_day'].count()
        return {'dia':dia, 'cantidad':str(resp)}



@app.get('/score_titulo/{titulo}')
# Tiene como parametro un titulo de una pelicula y retorna en un diccionario con el titulo,popularidad y año de estreno de la pelicula
def score_titulo(titulo:str):
    if not isinstance(titulo, str):
        return 'Debe ingresar un texto'
    elif not (df_movie == titulo).any().any():
        return 'La pelicula no se encuentra en la base de datos'
    else:
        resp = df_movie[df_movie['title'] == titulo][['title','popularity','release_year']].to_dict(orient='records')[0]
        return {'titulo':resp['title'], 'popularidad':str(resp['popularity']), 'año':str(resp['release_year'])}


@app.get('/votos_titulo/{titulo}')
# Tiene como parametro un titulo de una pelicula y retorna en un diccionario con el titulo, votos totales, votacion promedio por pelicula
def votos_titulo(titulo:str):
    if not isinstance(titulo, str):
        return 'Debe ingresar un texto'
    elif not (df_movie == titulo).any().any():
        return 'La pelicula no se encuentra en la base de datos'
    elif int(df_movie[df_movie['title'] == titulo]['vote_count']) > 2000:
        resp = df_movie[df_movie['title'] == titulo][['title','vote_count','vote_average']].to_dict(orient='records')[0]
        return {'titulo':resp['title'], 'voto_total':str(resp['vote_count']), 'voto_promedio':str(resp['vote_average'])}
    else:
        return 'La consulta no cumple con las condicion por ende no se devuelve informacion'



@app.get('/get_actor/{nombre_actor}')
# Tiene como parametro un nombre de actor y retorna en un diccionario el nombre del actor, la cantidad de filmaciones en las que participo, 
# retorno de cada pelicula y promedio de retorno por pelicula
def get_actor(nombre_actor:str):
    if not isinstance(nombre_actor, str):
        return 'Debe ingresar un texto'
    
    elif not any(nombre_actor in sublist for sublist in df_movie['actors'] if sublist):
        return 'El actor no se encuentra en la base de datos'

    _return = 0
    n_films = 0
    avg = 0
    for index,lista in enumerate(df_movie['actors']):
        if lista: 
            if nombre_actor in lista:
                n_films += 1
                _return += df_movie['return'].iloc[index]
    
    if _return == 0 and n_films == 0:
        avg = 0
    else:
        avg = _return/n_films

    return {'actor':nombre_actor, 'cantidad_filmaciones':str(n_films), 'retorno_total':str(_return), 'retorno_promedio':str(avg)}



@app.get('/get_director/{nombre_director}')
# esta funcion tiene como parametro un nombre de director de alguna pelicula y retorna en nombre del director, retorno total de las peliculas en las que participo
# nombre de las peliculas y revenue de cada pelicula.
def get_director(nombre_director:str):
    if not isinstance(nombre_director, str):
        return 'Debe ingresar un texto'
    elif not any(nombre_director in sublist for sublist in df_movie['directors'] if sublist):
        return 'El director no se encuentra en la base de datos'

    total_return = 0
    movies = []
    years = []
    _return = []
    budget = []
    revenue = []
    for index,lista in enumerate(df_movie['directors']):
        if lista:
            if nombre_director in lista:
                total_return += df_movie['return'][index]
                movies.append(df_movie['title'][index])
                years.append(df_movie['release_year'][index])
                _return.append(df_movie['return'][index])
                budget.append(df_movie['budget'][index])
                revenue.append(df_movie['revenue'][index])

    return {'director':nombre_director, 'retorno_total_director':str(total_return), 
    'peliculas':str(movies), 'año':str(years), 'retorno_pelicula':str(_return), 
    'budget_pelicula':str(budget), 'revenue_pelicula':str(revenue)}

@app.get('/recomendacion/{titulo}')
# Funcion que tiene como parametro un titulo de pelicula y retorna 5 recomendaciones a partir de esta con un sistema de machine learning.
def recomendacion(titulo:str):
    if not isinstance(titulo, str):
        return 'Debe ingresar un texto'
    elif not (df_movie == titulo).any().any():
        return 'La pelicula no se encuentra en la base de datos'
    # Cargo los modelos entrenados
    tfidf_model = joblib.load("./Models/tfidf_model.pkl")
    knn_model = joblib.load("./Models/knn_model.pkl")

    title_vector = tfidf_model.transform([titulo])  # Transforma el título de entrada en una representación vectorial
    _, indices = knn_model.kneighbors(title_vector)  # Busca los vecinos más cercanos basados en la representación vectorial
    recommendations = df_movie["title"].iloc[indices[0][1:]].tolist()  # Obtiene los títulos de las películas más similares (excluyendo la película de referencia)
    return {'lista recomendada': str(recommendations)}