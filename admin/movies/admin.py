from django.contrib import admin

from .models import Filmwork, Genre, GenreFilmwork, Person, PersonFilmwork


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork
    autocomplete_fields = ['genre']

class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork 
    autocomplete_fields = ['person']


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline, PersonFilmworkInline, ) 
    list_display = ('title', 'type', 'created', 'rating', 'get_genres', )
    list_filter = ('type',)
    search_fields = ('title', 'description', 'uuid') 
    list_prefetch_related = ('genres', )

    def get_queryset(self, request):
        queryset = (
                    super()
                    .get_queryset(request)
                    .prefetch_related(*self.list_prefetch_related)
        )
        return queryset

    def get_genres(self, obj):
        return ','.join([genre.name for genre in obj.genres.all()])

    get_genres.short_description = 'Жанры фильма'

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    search_fields = ('full_name', )


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ('name', ) 
