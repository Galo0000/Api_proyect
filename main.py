from fastapi import FastAPI
import pandas as pd

df_movie = pd.read_csv('api.csv')
df_movie['release_date'] = pd.to_datetime(df_movie['release_date'], format='%Y-%m-%d')
app = FastAPI()


@app.get("/")
def index():
    cfun1 = ["Cantidad de peliculas segun mes /cantidad_filmaciones_mes/{mes}"]
    cfun2 = ["Cantidad de peliculas segun dia semanal /cantidad_filmaciones_dia{dia}"]
    cfun3 = ["Año escore segun titulo de pelicula /score_titulo/{titulo}"]
    cfun4 = ["Cantidad de votos y promedio segun titulo de pelicula /votos_titulo/{titulo}"]
    cfun5 = ["Retorno,cantidad de películas y promedio de retorno por pelicula segun titulo de pelicula /get_actor/{nombre_actor"]  
    cfun6 = ["Actor /get_director(nombre_director)"]
    cfun7 = ['Director /recomendacion/{titulo}']

    milista = cfun1+cfun2+cfun3+cfun4+cfun5+cfun6+cfun7
    return milista

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

    return {'dia':dia, 'cantidad':str(resp)}

@app.get('/score_titulo/{titulo}')
def score_titulo(titulo:str):
    resp = df_movie[df_movie['title'] == titulo][['title','popularity','release_year']].to_dict(orient='records')[0]
    return {'titulo':resp['title'], 'año':str(resp['popularity']), 'popularidad':str(resp['release_year'])}


@app.get('/votos_titulo/{titulo}')
def votos_titulo(titulo:str):
    if int(df_movie[df_movie['title'] == titulo]['vote_count']) > 2000:
        resp = df_movie[df_movie['title'] == titulo][['title','vote_count','vote_average']].to_dict(orient='records')[0]
        return {'titulo':resp['title'], 'voto_total':str(resp['vote_count']), 'voto_promedio':str(resp['vote_average'])}
    else:
        return 'La consulta no cumple con las condicion por ende no se devuelve informacion'



@app.get('/get_actor/{nombre_actor}')
def get_actor(nombre_actor:str):
    total_return = 0
    n_films = 0
    avg = 0
    for index,lista in enumerate(df_movie['actor']):
        if type(lista) == list: 
            if nombre_actor in lista:
                n_films += 1
                _return += df_movie['return'][index]
    
    if total_return == 0 and n_films == 0:
        avg = 0
    else:
        avg = total_return/n_films

    return {'actor':nombre_actor, 'cantidad_filmaciones':str(n_films), 'retorno_total':str(total_return), 'retorno_promedio':str(avg)}



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

    return {'director':nombre_director, 'retorno_total_director':str(total_return), 
    'peliculas':movies, 'anio':str(years), 'retorno_pelicula':str(_return), 
    'budget_pelicula':str(budget), 'revenue_pelicula':str(revenue)}