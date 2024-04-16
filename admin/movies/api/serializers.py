from rest_framework import serializers

from movies.models import Filmwork, Genre
from movies.models import PersonFilmwork as PersF


class GenreSerializer(serializers.ModelSerializer):

    class Meta: 
        model = Genre
        fields = ('name',)


class GenresField(serializers.RelatedField):

    def to_representation(self, value):
        return value.name


class FilmworkSerializer(serializers.ModelSerializer):
    genres = GenresField(queryset=Genre, many=True)
    actors = serializers.SerializerMethodField()
    directors = serializers.SerializerMethodField()
    writers = serializers.SerializerMethodField()

    class Meta: 
        model = Filmwork
        fields = (
            'id', 'title', 'description', 'creation_date', 'rating',
            'type', 'genres', 'actors', 'directors', 'writers')
    
    def get_actors(self, obj):
        all_actors  = PersF.objects.select_related(
            'film_work').select_related('person').filter(
            film_work=obj.id, role='actor')
        # all_persons = PersF.objects.all()
        # all_actors = all_persons.filter(film_work=obj.id, role='actor')
        actors_list = [one.person.full_name for one in all_actors]
        return actors_list
    
    def get_directors(self, obj):
        all_directors  = PersF.objects.select_related(
            'film_work').select_related('person').filter(
            film_work=obj.id, role='director')
        directors_list = [one.person.full_name for one in all_directors]
        return directors_list
    
    def get_writers(self, obj):
        all_writers  = PersF.objects.select_related(
            'film_work').select_related('person').filter(
            film_work=obj.id, role='writer')
        writer_list = [one.person.full_name for one in all_writers]
        return writer_list