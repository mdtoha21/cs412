
from django.urls import path
from django.conf import settings
from . import views
from .views import ProfileListView

urlpatterns=[
    
path('', ProfileListView.as_view(), name='show_all_profiles'),



]