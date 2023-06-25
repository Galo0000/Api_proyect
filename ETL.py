# se importan las librerias a utilizar en el proceso de ETL
import pandas as pd
import numpy as np


# Se carga en la variable df_movies utilizando pandas, la informacion contenida en el archivo movies_dataset.csv
df_movies = pd.read_csv('./Dataset/movies_dataset.csv',delimiter=',')

df_credits = pd.read_csv('./Dataset/credits.csv',delimiter=',')


# Se crea una variable del tipo lista llamada 'columns' en la cual se carga los nombres de las columnas a tratar en el siguente codigo.
columns = ['revenue','budget']
# se utiliza la funcion fillna() para reemplazar los valores nulos por el numero entero 0.
df_movies[columns] = df_movies[columns].fillna(0)


#df_movies['release_date'] = df_movies['release_date'].fillna('no_release_date')
df_movies.dropna(subset=['release_date'], inplace=True)


enteros = ['1','12','22']
for a in enteros:
    df_movies = df_movies.drop(df_movies[df_movies['release_date'] == a].index)


df_movies['release_date'] = pd.to_datetime(df_movies['release_date'], format='%Y-%m-%d')

df_movies['release_year'] = df_movies['release_date'].dt.year

df_movies[['revenue','budget']] = df_movies[['revenue','budget']].astype(float)

df_movies['return'] = np.where((df_movies['revenue'] != 0) & (df_movies['budget'] != 0), df_movies['revenue'] / df_movies['budget'], 0)

df_movies.drop(['video','imdb_id','adult','original_title','poster_path','homepage'],axis=1,inplace=True)