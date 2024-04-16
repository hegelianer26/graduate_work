from faker import Faker

fake = Faker()


data = [{
            'uuid': fake.uuid4(),
            'imdb_rating': fake.random_int(0, 9),
            'genre_names': ['Action'],
            'genre': [{'name': 'Action',
                      'uuid': fake.uuid4(),
                      } for _ in range(1)],
            'title': fake.word(),
            'description': fake.sentence(nb_words=20),
            'director_name': fake.name(),
            'actors_names': [fake.name() for _ in range(3)],
            'writers_names': [fake.name() for _ in range(3)],
            'actors':
                [{'uuid': fake.uuid4(),
                  'full_name': fake.name(),} for _ in range(3)],
            'writers':
                [{'uuid': fake.uuid4(),
                  'full_name': fake.name(),} for _ in range(3)],
            'directors':
                [{'uuid': fake.uuid4(),
                  'full_name': fake.name(),} for _ in range(3)],

        } for _ in range(100)]


data[0] ={
    "uuid": "025c58cd-1b7e-43be-9ffb-8571a613579b",
    "imdb_rating": 10,
    "genre_names": ["Action", "Adventure", "Fantasy", "Sci-Fi"],
    "genre": [{"name": "Action", "uuid": "3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff"},
          {"name": "Adventure", "uuid": "120a21cf-9097-479e-904a-13dd7198c1dd"},
          {"name": "Fantasy", "uuid": "b92ef010-5e4c-4fd0-99d6-41b6456272cd"},
          {"name": "Sci-Fi", "uuid": "6c162475-c7ed-4461-9184-001ef3d9f26e"}],
    "title": "Star Wars: Episode VI - Return of the Jedi",
    "description": "Luke Skywalker battles horrible Jabba the Hut and cruel Darth Vader to save his comrades in the Rebel Alliance and triumph over the Galactic Empire. Han Solo and Princess Leia reaffirm their love and team with Chewbacca, Lando Calrissian, the Ewoks and the androids C-3PO and R2-D2 to aid in the disruption of the Dark Side and the defeat of the evil emperor.",
    "director_name": "Richard Marquand",
    "actors_names": ["Billy Dee Williams, Carrie Fisher, Harrison Ford, Mark Hamill"],
    "writers_names": ["George Lucas, Lawrence Kasdan"],
    "actors": [{"uuid": "26e83050-29ef-4163-a99d-b546cac208f8", "full_name": "Mark Hamill"},
           {"uuid": "5b4bf1bc-3397-4e83-9b17-8b10c6544ed1", "full_name": "Harrison Ford"},
           {"uuid": "b5d2b63a-ed1f-4e46-8320-cf52a32be358", "full_name": "Carrie Fisher"},
           {"uuid": "efdd1787-8871-4aa9-b1d7-f68e55b913ed", "full_name": "Billy Dee Williams"}],
    "writers": [{"uuid": "3217bc91-bcfc-44eb-a609-82d228115c50", "full_name": "Lawrence Kasdan"},
            {"uuid": "a5a8f573-3cee-4ccc-8a2b-91cb9f55250a", "full_name": "George Lucas"}],
    "directors": [{"uuid": "3214cf58-8dbf-40ab-9185-77213933507e", "full_name": "Richard Marquand"}]}
