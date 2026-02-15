from django.db import models


class Profile(models.Model):
    """Model for an individual user profile in mini_insta."""

    username = models.CharField(max_length=100)
    display_name = models.CharField(max_length=150)
    profile_image_url = models.URLField(max_length=500, blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateField()

    def __str__(self):
        return self.display_name or self.username
