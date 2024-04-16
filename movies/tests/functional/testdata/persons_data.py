from faker import Faker

fake = Faker()


data = [{
            'uuid': fake.uuid4(),
            'film_ids': ", ".join([fake.uuid4() for _ in range(3)]),
            'full_name': fake.name(),
            'role': ", ".join([fake.job() for _ in range(3)]),
            'film': [{'uuid': fake.uuid4(),
                      'title': fake.word(),
                      'imdb_rating': fake.random_int(0, 9)
                      } for _ in range(3)]
        } for _ in range(100)]

data[0] = {"uuid": "ffe0d805-3595-4cc2-a892-f2bedbec4ac6",
"film_ids": "7ee0af24-1b85-4406-b442-04574d41dd3b, 0312ed51-8833-413f-bff5-0e139c11264a",
"full_name": "Alun Daviess",
"role": "actor, writer",
"film": [{
    "uuid": "7ee0af24-1b85-4406-b442-04574d41dd3b",
    "title": "In Concert Cat Stevens: Moon & Star",
    "imdb_rating": 7.9},
    {"uuid": "0312ed51-8833-413f-bff5-0e139c11264a",
    "title": "Best film",
    "imdb_rating": 10}]
}
