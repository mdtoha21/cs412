from django.urls import path
from django.conf import settings
from . import views


urlpatterns=[

    #path(r'',views.home,name="home"),

    path(r'',views.home_page,name="home_page"),
    path("quote/", views.quote,name="quote"),
    path("show_all/", views.show_all,name="show_all"),
    path("about/", views.about,name="about"),

]