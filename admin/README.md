# Реализация API для кинотеатра

1. docker-compose up
2. docker-compose exec api python manage.py runserver migrate
3. docker-compose exec api python manage.py runserver createsuperuser
4. docker-compose exec api python manage.py runserver collectstatic
5. api доступно по адресу http://127.0.0.1/api/v1/movies/