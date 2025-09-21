from django.urls import path
from django.conf import settings
from . import views


urlpatterns=[


    path(r'',views.home,name="home"),
    path('order/', views.order, name="order"),
    path('submit/', views.submit, name="submit"),
  
  

]