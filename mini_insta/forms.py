from django import forms
from .models import *



class  CreatePostForm(forms.ModelForm):

    class Meta:
        model=Post
        fields = ['caption']


class UpdateProfileForm(forms.ModelForm):

    class Meta:
        model=Profile
        fields=['display_name','bio_text','profile_image_url']
        