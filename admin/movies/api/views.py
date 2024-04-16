from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response

from movies.models import Filmwork, Genre, GenreFilmwork

from .serializers import FilmworkSerializer


class MoviesViewSet(viewsets.ModelViewSet):

    queryset = Filmwork.objects.prefetch_related('genres').all()
    serializer_class = FilmworkSerializer
    http_method_names = ['get', ]
