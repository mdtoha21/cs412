from django.contrib import admin
from .models import Profile,Photo,Post,Follow,Comment,Like

admin.site.register(Profile)
# Register your models here.
admin.site.register(Post)

admin.site.register(Photo)
admin.site.register(Follow)
admin.site.register(Comment)
admin.site.register(Like)

