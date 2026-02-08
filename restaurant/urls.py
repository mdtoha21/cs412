
# 
# File: urls.py
# Author: MD Toha (mdtoha@bu.edu)
# Description: URL configuration for the restaurant app. 
#              Maps URL paths to the corresponding view functions.
#

from django.urls import path
from . import views

urlpatterns = [
    path('main/', views.main, name='main'),
    path('order/', views.order, name='order'),
    path('confirmation/', views.confirmation, name='confirmation'),
]