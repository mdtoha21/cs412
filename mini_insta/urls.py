from django.urls import path
from . import views

app_name = 'mini_insta'

urlpatterns = [
    path('', views.ProfileListView.as_view(), name='show_all_profiles'),
]
