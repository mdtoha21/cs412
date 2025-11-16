from django.db import models

class Joke(models.Model):

    text = models.TextField()
    contributor = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return f"{self.text}"
    

class Picture(models.Model):

    image_url = models.URLField()
    contributor = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.image_url



# Create your models here.
