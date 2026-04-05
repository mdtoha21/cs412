from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="dadjokes_index"),
    path("random", views.random_pair, name="dadjokes_random"),
    path("jokes", views.jokes_list, name="dadjokes_jokes"),
    path("joke/<int:pk>", views.joke_detail, name="dadjokes_joke_detail"),
    path("pictures", views.pictures_list, name="dadjokes_pictures"),
    path("picture/<int:pk>", views.picture_detail, name="dadjokes_picture_detail"),
    path("api/", views.api_index, name="dadjokes_api_index"),
    path("api/random", views.api_random, name="dadjokes_api_random"),
    path("api/jokes", views.api_jokes, name="dadjokes_api_jokes"),
    path("api/joke/<int:pk>", views.api_joke_detail, name="dadjokes_api_joke_detail"),
    path("api/pictures", views.api_pictures, name="dadjokes_api_pictures"),
    path("api/picture/<int:pk>", views.api_picture_detail, name="dadjokes_api_picture_detail"),
    path("api/random_picture", views.api_random_picture, name="dadjokes_api_random_picture"),
]