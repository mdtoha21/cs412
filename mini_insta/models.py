from django.db import models
from django.urls import reverse
# Create your models here.
class Profile(models.Model):

    #define the data attribute
    username=models.TextField(blank=True)
    display_name=models.TextField(blank=True)
    profile_image_url=models.URLField(blank=True)
    bio_text=models.TextField(blank=True)
    join_date=models.DateTimeField(auto_now=True)


    def __str__(self):
        

        return f'{self.display_name}'
    

    def get_all_post(self):

       posts=Post.objects.filter(profile=self).order_by('-timestamp')

       return posts
    def get_absolute_url(self):
        # redirect back to the profile page after update
        return reverse('show_profile', args=[self.pk])
    
    
class Post(models.Model):


    profile=models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp=models.DateTimeField(auto_now=True)
    caption=models.TextField(blank=True)



    def __str__(self):

        return f'{self.profile}'
    
    def get_all_photo(self):

        photos=Photo.objects.filter(post=self)

        return photos
    

    
class Photo(models.Model):

    '''    Represents a photo attached to a post.'''

    post=models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url=models.URLField(blank=True)
    image_file=models.ImageField(blank=True)
    timestamp=models.DateTimeField(auto_now=True)





    def __str__(self):

        if self.image_file:
            return f"Photo (file): {self.image_file.url}"
        elif self.image_url:

            return f"Photo (file): {self.image_url}"
        else:
            return 'No image'

    def get_image_url(self):

        if self.image_file:
            return self.image_file.url
        
        return self.image_url