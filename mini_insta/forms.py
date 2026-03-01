from django import forms
from .models import *



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