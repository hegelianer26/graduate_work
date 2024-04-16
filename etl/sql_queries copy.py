movies
movies_genres
genres
persons
movies_persons


small_sql_query = """ SELECT
    fw.modified as modified
    FROM content.film_work fw
    UNION SELECT
    p.modified as modified
    FROM content.person p
    UNION SELECT
    g.modified as modified
    FROM content.genre g
    ORDER BY modified DESC; """

small_genre_query = """ SELECT
    g.modified as modified
    FROM content.genre g
    ORDER BY modified DESC; """

small_person_query = """ SELECT
    GREATEST(MAX(p.modified), MAX(fw.modified), MAX(pfw.created)) as modified
    FROM content.person p
    LEFT JOIN content.person_film_work pfw ON pfw.person_id = p.id
    LEFT JOIN content.film_work fw ON pfw.film_work_id = fw.id
    GROUP BY p.id
    ORDER BY modified DESC; """



small_movie_query = """ SELECT
    GREATEST(MAX(g.modified), MAX(fw.modified), MAX(p.modified), MAX(pfw.created), MAX(gfw.created)) as great
    FROM content.film_work fw
    LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
    LEFT JOIN content.person p ON p.id = pfw.person_id
    LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
    LEFT JOIN content.genre g ON g.id = gfw.genre_id
    GROUP BY fw.id
    ORDER BY great DESC;
       """

big_sql_query = """SELECT
   fw.id as uuid,
   fw.rating as imdb_rating,
   array_agg(DISTINCT g.name) as genre_names,
   fw.duration as duration,
   COALESCE (
       json_agg(
           DISTINCT jsonb_build_object(
                'uuid', g.id,
                'name', g.name
           )
       ), '[]'
   ) as genre,
   fw.title,
   fw.description,
   GREATEST(MAX(g.modified), MAX(fw.modified), MAX(p.modified), MAX(pfw.created), MAX(gfw.created)) as great,
   COALESCE(
    STRING_AGG(DISTINCT p.full_name, ', ') FILTER (WHERE p.id is not null and pfw.role='director'), '' ) as director_name,
    STRING_AGG(DISTINCT p.full_name, ', ') FILTER (WHERE p.id is not null and pfw.role='actor') as actors_names,
    STRING_AGG(DISTINCT p.full_name, ', ') FILTER (WHERE p.id is not null and pfw.role='writer') as writers_names,
   COALESCE (
       json_agg(
           DISTINCT jsonb_build_object(
                'uuid', p.id,
                'full_name', p.full_name
           )
       ) FILTER (WHERE p.id is not null AND pfw.role='actor'),
       '[]'
   ) as actors,
   COALESCE (
       json_agg(
           DISTINCT jsonb_build_object(
                'uuid', p.id,
                'full_name', p.full_name
           )
       ) FILTER (WHERE p.id is not null AND pfw.role='writer'),
       '[]'
   ) as writers,
   COALESCE (
       json_agg(
           DISTINCT jsonb_build_object(
                'uuid', p.id,
                'full_name', p.full_name
           )
       ) FILTER (WHERE p.id is not null AND pfw.role='director'),
       '[]'
   ) as directors
FROM content.film_work fw
LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
LEFT JOIN content.person p ON p.id = pfw.person_id
LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
LEFT JOIN content.genre g ON g.id = gfw.genre_id
WHERE g.modified > '{upd}' or fw.modified > '{upd}' or p.modified > '{upd}' or pfw.created > '{upd}' or gfw.created > '{upd}'
GROUP BY uuid
ORDER BY great DESC; """


genre_sql_query = """ SELECT
    g.id as uuid,
    g.name as name,
    MAX(g.modified) as great
    FROM content.genre g
    WHERE g.modified > '{upd}'
    GROUP BY g.id
    ORDER BY great DESC;
    """

person_sql_query = """ SELECT
    p.id as uuid,
    p.full_name as full_name,
    GREATEST(MAX(p.modified), MAX(fw.modified), MAX(pfw.created)) as great,
    STRING_AGG(pfw.film_work_id::varchar, ', ') as film_ids,
    STRING_AGG(DISTINCT pfw.role, ', ') as role,
    COALESCE (
        json_agg(
            DISTINCT jsonb_build_object('uuid', pfw.film_work_id, 'title', fw.title, 'imdb_rating', fw.rating)
            ), '[]') as film
    FROM content.person p
    LEFT JOIN content.person_film_work pfw ON pfw.person_id = p.id
    LEFT JOIN content.film_work fw ON pfw.film_work_id = fw.id
    GROUP BY uuid
    HAVING GREATEST(MAX(p.modified), MAX(fw.modified), MAX(pfw.created)) > '{upd}'
    ORDER BY great DESC;
    """
