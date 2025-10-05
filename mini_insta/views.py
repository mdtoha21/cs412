from django.shortcuts import render
from django.views.generic import ListView
from .models import Profile, Post, Photo
from django.views.generic import DetailView


# Create your views here.


class  ProfileListView(ListView):
    '''Define a view class to show all mini_insta profiles'''
    model=Profile
    template_name="mini_insta/show_all_profiles.html"
    context_object_name="profiles"


class ProfileDetailView(DetailView):
    '''Define a view class to show a single mini_insta profiles'''

    model=Profile
    template_name="mini_insta/show_profile.html"
    context_object_name="profile"



class PostDetailView(DetailView):
    model=Post
    template_name="mini_insta/show_post.html"
    context_object_name="post"







