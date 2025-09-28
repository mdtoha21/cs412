from django.shortcuts import render
from django.views.generic import ListView
from .models import Profile


# Create your views here.


class  ProfileListView(ListView):
    '''Define a view class to show all mini_insta profiles'''
    model=Profile
    template_name="mini_insta/show_all_profiles.html"
    context_object_name="profiles"
    


