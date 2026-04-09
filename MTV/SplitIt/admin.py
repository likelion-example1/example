from django.contrib import admin
from .models import Post, Comment, Hashtag, Location


admin.site.register(Post)

admin.site.register(Comment)

admin.site.register(Hashtag)

admin.site.register(Location)
# Register your models here.
