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
    
    def get_followers(self):
        ''''Retrieve all profiles that are following this profile.'''

        follows=Follow.objects.filter(profile=self)
        followers=[f.follower_profile for f in follows]


        return followers
    
    def get_num_followers(self):
        """Return the number of followers."""
        return Follow.objects.filter(profile=self).count()
    
    def get_following(self):
        """Return a list of Profiles this profile is following."""
        follows = Follow.objects.filter(follower_profile=self)
        following = [f.profile for f in follows]
        return following
    

    def get_num_following(self):
        """Return the number of profiles this profile is following."""
        return Follow.objects.filter(follower_profile=self).count()

    
    
class Post(models.Model):


    profile=models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp=models.DateTimeField(auto_now=True)
    caption=models.TextField(blank=True)



    def __str__(self):

        return f'{self.profile}'
    
    def get_all_photo(self):

        photos=Photo.objects.filter(post=self)

        return photos
    def get_all_comments(self):
        """Retrieve all comments on this post, ordered by most recent first."""
        return Comment.objects.filter(post=self).order_by('-timestamp')
    
    def get_likes(self):
     
     """Return a QuerySet of all likes on this post."""
     return Like.objects.filter(post=self)
    

    
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
    

class Follow(models.Model):
    '''Represents a following relationship between two Profile objects.'''

    profile=models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="main_profile")
    follower_profile=models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="follower_profile")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        follower_name = self.follower_profile.display_name or self.follower_profile.username
        profile_name = self.profile.display_name or self.profile.username
        return f"{follower_name} follows {profile_name}"


class Comment(models.Model):

    '''  Represents a comment made by a Profile on a Post'''
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    text = models.TextField(blank=False)

    def __str__(self):
        return f'Comment by {self.profile.display_name} on {self.post.id}: {self.text[:30]}...'
    



class Like(models.Model):

    ''' Represents a "like" action by a Profile on a Post.'''
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.profile.display_name} liked Post {self.post.id}'