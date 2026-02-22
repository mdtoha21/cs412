from django.contrib import admin
from .models import Profile,Photo,Post

admin.site.register(Profile)
# Register your models here.
admin.site.register(Post)

admin.site.register(Photo)
