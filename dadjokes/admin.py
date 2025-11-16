from django.contrib import admin

# Register your models here.

from .models import Joke, Picture

@admin.register(Joke)
class JokeAdmin(admin.ModelAdmin):
    list_display = ("id", "contributor", "created_at")
    list_display_links = ("id",)

@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    list_display = ("id", "contributor", "image_url", "created_at")
    list_display_links = ("id",)
