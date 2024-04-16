import uuid
from datetime import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(_('created'), default=datetime.now)
    modified = models.DateTimeField(_('modified'), default=datetime.now)

    class Meta:
        # Этот параметр указывает Django, что этот класс не является представлением таблицы
        abstract = True


class UUIDMixin(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id = models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36)
    
    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('name'), max_length=255, db_index=True)
    description = models.TextField(_('description'), blank=True, null=True)

    class Meta:
        # Ваши таблицы находятся в нестандартной схеме. Это нужно указать в классе модели
        db_table = "genres"
        # Следующие два поля отвечают за название модели в интерфейсе
        verbose_name = _('genre')
        verbose_name_plural = _('genres')

    def __str__(self):
        return self.name 


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_('full_name'), max_length=255, db_index=True)

    def __str__(self):
        return self.full_name 

    class Meta:
        # Ваши таблицы находятся в нестандартной схеме. Это нужно указать в классе модели
        db_table = "persons"
        # Следующие два поля отвечают за название модели в интерфейсе
        verbose_name = _('person')
        verbose_name_plural = _('persons')


class Filmwork(TimeStampedMixin):
    # uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    uuid = models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36)

    title = models.CharField(_('name'), max_length=255, db_index=True)
    description = models.TextField(_('description'), blank=True, null=True)
    creation_date = models.IntegerField(_('creation_date'), blank=True, null=True)
    file_path = models.TextField(_('file_path'), blank=True, null=True)
    rating = models.FloatField(_('rating'), blank=True, null=True,
                               validators=[MinValueValidator(0),
                                           MaxValueValidator(100)]) 
    type = models.TextField(_('type'), blank=True, null=True)
    genres = models.ManyToManyField(Genre, through='GenreFilmwork')
    persons = models.ManyToManyField(Person, through='PersonFilmwork')
    duration = models.IntegerField(_('duration'), blank=True, null=True)

    class Meta:
        # Ваши таблицы находятся в нестандартной схеме. Это нужно указать в классе модели
        db_table = "movies"
        # Следующие два поля отвечают за название модели в интерфейсе
        verbose_name = _('movie')
        verbose_name_plural = _('movies') 

    def __str__(self):
        return self.title 


class GenreFilmwork(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    film_work = models.ForeignKey(Filmwork, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ваши таблицы находятся в нестандартной схеме. Это нужно указать в классе модели
        db_table = "movies_genres"
        unique_together = ['film_work_id', 'genre_id', ]
        indexes = [
            models.Index(fields=['film_work_id', 'genre_id']),
        ]

class PersonFilmwork(models.Model):

    class RoleInFilm(models.TextChoices):
        director = 'director', _('director')
        writer = 'writer', _('writer')
        actor = 'actor', _('actor')
        
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    film_work = models.ForeignKey(Filmwork, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    role = models.TextField(_('role'), max_length=10, choices=RoleInFilm.choices, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ваши таблицы находятся в нестандартной схеме. Это нужно указать в классе модели
        db_table = "movies_persons"
        # unique_together = ['film_work_id', 'person_id', 'role']

        indexes = [
            models.Index(fields=['film_work_id', 'person_id', 'role']),
        ]