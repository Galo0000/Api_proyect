from fastapi import FastAPI
import pandas as pd
import pickle

#df_movie = pd.read_json('../Data/api.pickle')


with open('./Data/api37.pickle', 'rb') as archivo:
    df_movie = pickle.load(archivo)

with open('./Data/list_actors37.pickle', 'rb') as archivo:
    list_actors = pickle.load(archivo)

with open('./Data/list_directors37.pickle', 'rb') as archivo:
    list_directors = pickle.load(archivo)

app = FastAPI()

@app.get('/cantidad_filmaciones_mes/{mes}')
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
        resp = df_movie[(df_movie['status'] == 'Released') & (df_movie['release_month'] == month)]['release_month'].count()
        return {'mes': mes, 'cantidad': str(resp)}




@app.get('/cantidad_filmaciones_dia{dia}')
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
        resp = df_movie[(df_movie['status'] == 'Released') & (df_movie['release_day'] == day)]['release_day'].count()
        return {'dia':dia, 'cantidad':resp}

@app.get('/score_titulo/{titulo}')
def score_titulo(titulo:str):
    if not isinstance(titulo, str):
        return 'Debe ingresar un texto'
    elif not (df_movie == titulo).any().any():
        return 'La pelicula no se encuentra en la base de datos'
    else:
        resp = df_movie[df_movie['title'] == titulo][['title','popularity','release_year']].to_dict(orient='records')[0]
        return {'titulo':resp['title'], 'popularidad':resp['popularity'], 'año':resp['release_year']}


@app.get('/votos_titulo/{titulo}')
def votos_titulo(titulo:str):
    if not isinstance(titulo, str):
        return 'Debe ingresar un texto'
    elif not (df_movie == titulo).any().any():
        return 'La pelicula no se encuentra en la base de datos'
    elif int(df_movie[df_movie['title'] == titulo]['vote_count']) > 2000:
        resp = df_movie[df_movie['title'] == titulo][['title','vote_count','vote_average']].to_dict(orient='records')[0]
        return {'titulo':resp['title'], 'voto_total':resp['vote_count'], 'voto_promedio':resp['vote_average']}
    else:
        return 'La consulta no cumple con las condicion por ende no se devuelve informacion'



@app.get('/get_actor/{nombre_actor}')
def get_actor(nombre_actor:str):
    if not isinstance(nombre_actor, str):
        return 'Debe ingresar un texto'
    elif nombre_actor not in list_actors:
        return 'El actor no se encuentra en la base de datos'

    _return = 0
    n_films = 0
    avg = 0
    for index,lista in enumerate(df_movie['actors']):
        if type(lista) == list: 
            if nombre_actor in lista:
                n_films += 1
                _return += df_movie['return'][index]
    
    if _return == 0 and n_films == 0:
        avg = 0
    else:
        avg = _return/n_films

    return {'actor':nombre_actor, 'cantidad_filmaciones':n_films, 'retorno_total':_return, 'retorno_promedio':avg}



@app.get('/get_director/{nombre_director}')
def get_director(nombre_director:str):
    if not isinstance(nombre_director, str):
        return 'Debe ingresar un texto'
    elif nombre_director not in list_directors:
        return 'El director no se encuentra en la base de datos'

    total_return = 0
    movies = []
    years = []
    _return = []
    budget = []
    revenue = []
    for index,lista in enumerate(df_movie['directors']):
        if type(lista) == list:
            if nombre_director in lista:
                total_return += df_movie['return'][index]
                movies.append(df_movie['title'][index])
                years.append(df_movie['release_year'][index])
                _return.append(df_movie['return'][index])
                budget.append(df_movie['budget'][index])
                revenue.append(df_movie['revenue'][index])

    return {'director':nombre_director, 'retorno_total_director':total_return, 
    'peliculas':movies, 'año':years, 'retorno_pelicula':_return, 
    'budget_pelicula':budget, 'revenue_pelicula':revenue}