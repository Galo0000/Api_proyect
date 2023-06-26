from fastapi import FastAPI
import pandas as pd

df_movie = pd.read_csv('api.csv')
df_movie['release_date'] = pd.to_datetime(df_movie['release_date'], format='%Y-%m-%d')
app = FastAPI()


@app.get('/cantidad_filmaciones_mes/{mes}')
def cantidad_filmaciones_mes(mes:str):
    months = {
    "enero": 1,
    "febrero":2,
    "marzo":3,
    "abril":4,
    "mayo":5,
    "junio":6,
    "julio":7,
    "agosto":8,
    "septiembre":9,
    "octubre":10,
    "noviembre":11,
    "diciembre":12}
    
    month = months.get(mes)
    resp = df_movie[(df_movie['status'] == 'Released') & (df_movie['release_month'] == month)]['release_month'].count()

    return {'mes':mes, 'cantidad':str(resp)}




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

    day = days.get(dia)

    resp = df_movie[(df_movie['status'] == 'Released') & (df_movie['day'] == day)]['day'].count()

    return {'dia':dia, 'cantidad':resp}

@app.get('/score_titulo/{titulo}')
def score_titulo(titulo:str):
    resp = df_movie[df_movie['title'] == titulo][['title','popularity','release_year']].to_dict(orient='records')[0]
    return {'titulo':resp['title'], 'anio':resp['popularity'], 'popularidad':resp['release_year']}


@app.get('/votos_titulo/{titulo}')
def votos_titulo(titulo:str):
    if int(df_movie[df_movie['title'] == titulo]['vote_count']) > 2000:
        resp = df_movie[df_movie['title'] == titulo][['title','vote_count','vote_average']].to_dict(orient='records')[0]
        return {'titulo':resp['title'], 'voto_total':resp['vote_count'], 'voto_promedio':resp['vote_average']}
    else:
        return 'La consulta no cumple con las condicion por ende no se devuelve informacion'



@app.get('/get_actor/{nombre_actor}')
def get_actor(nombre_actor:str):
    total_return = 0
    n_films = 0
    avg = 0
    for index,lista in enumerate(df_movie['actor']):
        if nombre_actor in lista:
            n_films += 1
            total_return += df_movie['return'][index]
    
    if total_return == 0 and n_films == 0:
        avg = 0
    else:
        avg = total_return/n_films

    return {'actor':nombre_actor, 'cantidad_filmaciones':n_films, 'retorno_total':total_return, 'retorno_promedio':avg}



@app.get('/get_director/{nombre_director}')
def get_director(nombre_director:str):
    total_return = 0
    movies = []
    years = []
    _return = []
    budget = []
    revenue = []
    for index,lista in enumerate(df_movie['director']):
        if nombre_director in lista:
            total_return += df_movie['return'][index]
            movies.append(df_movie['title'][index])
            years.append(df_movie['release_year'][index])
            _return.append(df_movie['return'][index])
            budget.append(df_movie['budget'][index])
            revenue.append(df_movie['revenue'][index])

    return {'director':nombre_director, 'retorno_total_director':total_return, 
    'peliculas':movies, 'anio':years, 'retorno_pelicula':_return, 
    'budget_pelicula':budget, 'revenue_pelicula':revenue}