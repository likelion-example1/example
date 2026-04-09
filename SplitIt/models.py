from django.db import models
from django.contrib.auth.models import User #장고 기본모델 가져오는 코드

# Create your models here.
LANGUAGE_CHOICES = (

    (1, "KOR"),

    (2, "ENG"),

    (3, "JPN"),

    (4, "CHN"),

)


class Post(models.Model):

    title = models.CharField(max_length=200)

    date = models.DateTimeField(auto_now_add=True)

    body = models.TextField()

    language = models.IntegerField(choices=LANGUAGE_CHOICES)
    
    
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hosted_posts')

    
    participants = models.ManyToManyField(User, related_name='participated_posts', blank=True)


    def __str__(self):

        return self.title

class Comment(models.Model):

    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)

    username = models.CharField(max_length=20)

    comment_text = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):

        return self.comment_text[:20]