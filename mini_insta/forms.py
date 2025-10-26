from django import forms
from .models import *

from django.contrib.auth.models import User

class  CreatePostForm(forms.ModelForm):

    class Meta:
        model=Post
        fields = ['caption']


class UpdateProfileForm(forms.ModelForm):

    ''' Form to update a user's Profile.

    Only allows updating:
        - display_name
        - bio_text
        - profile_image_url'''

    class Meta:
        model=Profile
        fields=['display_name','bio_text','profile_image_url']

class UpdatePostForm(forms.ModelForm):
    ''' Form to update a Post.'''
    class Meta:
        model = Post
        fields = ['caption']


class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['username','display_name', 'bio_text', 'profile_image_url']