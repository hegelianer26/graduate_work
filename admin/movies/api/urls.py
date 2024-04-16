from django.urls import include, path
from rest_framework import routers

from .views import MoviesViewSet

router = routers.DefaultRouter()

router.register(r'v1/movies', MoviesViewSet)
router.register(r'v1/movies/<uuid:pk>', MoviesViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
]