from faker import Faker

fake = Faker()


data = [{
            'uuid': fake.uuid4(),
            'name': fake.word(),
        } for _ in range(900)]

data[0] = {'uuid': '9c627155-d6dc-432c-bdd0-09030aefdb8c', 'name': 'REAL'}