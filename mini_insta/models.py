from django.db import models

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


    post=models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url=models.URLField(blank=True)
    timestamp=models.DateTimeField(auto_now=True)


    def __str__(self):



        return f'{self.post}'