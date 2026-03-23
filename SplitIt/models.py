from django.db import models

# Create your models here.
class Post(models.Model):
 STATUS_CHOICES = (
   ('모집중','모집중'),
   ('모집완료','모집완료'),
 )
   

 title = models.CharField(max_length=50)

 created_at = models.DateTimeField(auto_now_add=True)

 content = models.TextField(max_length=500)

 writer = models.CharField(max_length=50, default="익명")        # 임시 작성자명
 store_name = models.CharField(max_length=100, default="미정")   # 식당 이름
 pickup_location = models.CharField(max_length=100, default="미정") # 수령 장소
 delivery_fee = models.IntegerField(default=0)                   # 배달비 (숫자만!)
 target_headcount = models.IntegerField(default=2)               # 모집 인원 (기본 2명-게시판에서 수정가능)

 status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='모집중')

def __str__(self):

    return self.title
