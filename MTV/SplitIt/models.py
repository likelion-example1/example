from django.db import models

# Create your models here.
class Hashtag(models.Model):

 hashtag = models.CharField(max_length=100)


 def __str__(self):

  return self.hashtag


class Location(models.Model):
  name = models.CharField(max_length =50)

  def __str__(self):
    return self.name


class Post(models.Model):
 STATUS_CHOICES = (
   ('모집중','모집중'),
   ('모집완료','모집완료'),
 )
   

 title = models.CharField(max_length=50)

 created_at = models.DateTimeField(auto_now_add=True)

 content = models.TextField(max_length=500)
 photo = models.ImageField(blank=True, null=True, upload_to="post_photo")
 hashtag = models.ManyToManyField(Hashtag)

 writer = models.CharField(max_length=50, default="익명")        # 임시 작성자명
 store_name = models.CharField(max_length=100, default="미정")   # 식당 이름
 location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="수령장소") # 수령 장소
 delivery_fee = models.IntegerField(default=0)                   # 배달비 (숫자만!)
 target_headcount = models.IntegerField(default=2)               # 모집 인원 (기본 2명-게시판에서 수정가능)

 status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='모집중')

class Comment(models.Model):

    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)

    username = models.CharField(max_length=20)

    comment_text = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)


    def approve(self):

      self.save()


    def __str__(self):

      return self.comment_text

def __str__(self):

    return self.title




class Participant(models.Model):
  post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name ='participants')
  nickname = models.CharField(max_length=50)
  menu = models.CharField(max_length=100)

  def __str__(self):
    return f"{self.nickname} - {self.menu}"