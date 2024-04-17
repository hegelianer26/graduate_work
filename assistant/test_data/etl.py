import pandas as pd
from sqlalchemy import create_engine
import uuid
import datetime
import ast
from core.config import postgres_config

df = pd.read_excel('kinopoisk1.xlsx')

engine = create_engine(
    f'postgresql://{postgres_config.user}:{postgres_config.password}@{postgres_config.host}:{postgres_config.port}/{postgres_config.dbname}')

df['movie_id'] = [uuid.uuid4() for _ in range(len(df))]
df['created'] = [datetime.datetime.now() for _ in range(len(df))]
df['modified'] = [datetime.datetime.now() for _ in range(len(df))]
df['description'] = ['' for _ in range(len(df))]
df['file_path'] = ['' for _ in range(len(df))]
df['type'] = ['movie' for _ in range(len(df))]


df_movies = df[['movie_id', 'title', 'duration', 'rating', 'creation_date', 'created', 'modified', 'description', 'file_path', 'type']]
df_movies.columns = ['uuid', 'title', 'duration', 'rating', 'creation_date', 'created', 'modified', 'description', 'file_path', 'type']

df_persons = df[['full_name']]
df_persons = df_persons.drop_duplicates().reset_index(drop=True)
df_persons['person_id'] = [uuid.uuid4() for _ in range(len(df_persons))]
df_persons['created'] = [datetime.datetime.now() for _ in range(len(df_persons))]
df_persons['modified'] = [datetime.datetime.now() for _ in range(len(df_persons))]

df_link = df.merge(df_persons, on='full_name', how='left')[['movie_id', 'person_id']]
df_persons.columns = ['full_name', 'id', 'created', 'modified']
df_link['id'] = [uuid.uuid4() for _ in range(len(df_link))]
df_link['role'] = ['director' for _ in range(len(df_link))]
df_link['created'] = [datetime.datetime.now() for _ in range(len(df_link))]

df_link.columns = ['film_work_id', 'person_id', 'id',  'role', 'created']

df_movies.to_sql('movies', engine, if_exists='append', index=False)
df_persons.to_sql('persons', engine, if_exists='replace', index=False)
df_link.to_sql('movies_persons', engine, if_exists='replace', index=False)

df['genres'] = df['genres'].apply(ast.literal_eval)

unique_genres = set(genre for genre_list in df['genres'] for genre in genre_list)


genre_ids = [uuid.uuid4() for _ in range(len(unique_genres))]

df_genres = pd.DataFrame({'genre_id': genre_ids, 'name': list(unique_genres)})

df_genre_link = df.explode('genres').merge(df_genres, left_on='genres', right_on='name', how='inner')[['movie_id', 'genre_id']]

df_genres['created'] = [datetime.datetime.now() for _ in range(len(unique_genres))]
df_genres['modified'] = [datetime.datetime.now() for _ in range(len(unique_genres))]
df_genres['description'] = ['' for _ in range(len(unique_genres))]
df_genres.columns = ['id', 'name', 'created', 'modified', 'description']


df_genre_link['created'] = [datetime.datetime.now() for _ in range(len(df_genre_link))]
df_genre_link['id'] = [uuid.uuid4() for _ in range(len(df_genre_link))]
df_genre_link.columns = ['film_work_id', 'genre_id', 'created', 'id']

df_genres.to_sql('genres', engine, if_exists='replace', index=False)

df_genre_link.to_sql('movies_genres', engine, if_exists='replace', index=False)
