
from django.urls import path, include
from django.contrib.auth import views as auth_views   
from .views import * 
from . import views

urlpatterns = [
    # web urls
    path('', views.home, name='home'),
    path('random', views.random_page, name='random'),
    path('jokes', views.jokes_list, name='jokes'),
    path('joke/<int:pk>', views.joke_detail, name='joke_detail'),
    path('pictures', views.pictures_list, name='pictures'),
    path('picture/<int:pk>', views.picture_detail, name='picture_detail'),

    # api urls:
    path('api/', views.APIRandomJoke.as_view(), name='api_root_random'),       
    path('api/random', views.APIRandomJoke.as_view(), name='api_random'),
    path('api/jokes', views.APIJokeListCreate.as_view(), name='api_jokes'),
    path('api/joke/<int:pk>', views.APIJokeDetail.as_view(), name='api_joke_detail'),
    path('api/pictures', views.APIAllPictures.as_view(), name='api_pictures'),
    path('api/picture/<int:pk>', views.APIPictureDetail.as_view(), name='api_picture_detail'),
    path('api/random_picture', views.APIRandomPicture.as_view(), name='api_random_picture'),
]