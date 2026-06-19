from django.db import models
from django.conf import settings


# Create your models here.
LANGUAGE_CHOICES = (

    (1, "KOR"),

    (2, "ENG"),

    (3, "JPN"),

    (4, "CHN"),

)


class Post(models.Model):
    
    LOCATION_CHOICES = (
        ('ECC', 'ECC'), ('조형대', '조형대'), ('공대', '공대'), 
        ('연협', '연협'), ('학관', '학관'), ('학문관', '학문관'), ('중앙도서관', '중앙도서관')
    )
    
    CATEGORY_CHOICES = (
        ('한식', '한식'), ('분식', '분식'), ('양식', '양식'), 
        ('중식', '중식'), ('일식', '일식'), ('샐러드', '샐러드'), ('디저트_음료', '디저트 및 음료')
    )
    
    STATUS_CHOICES = (
        ('모집중', '모집중'), ('모집완료', '모집완료'),
    )

    title = models.CharField(max_length=200)

    date = models.DateTimeField(auto_now_add=True)

    body = models.TextField()

    language = models.IntegerField(choices=LANGUAGE_CHOICES)
    
    pickup_time = models.DateTimeField(null=True, blank=True) # 수령 시간
    location = models.CharField(max_length=20, choices=LOCATION_CHOICES, default='ECC') # 수령 장소
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='한식') # 카테고리
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='모집중') # 상태
   
   
    delivery_fee = models.IntegerField(default=0)      # 배달비
    min_order_amount = models.IntegerField(default=0)  # 최소주문 금액
    
    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='hosted_posts')

    
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='participated_posts', blank=True)

    photo = models.ImageField(blank=True, null=True, upload_to="post_photo")
 
 
    def __str__(self):

        return self.title

class Comment(models.Model):

    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    comment_text = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):

        return f"{self.author.username}: {self.comment_text[:20]}"
    
# 1. 매칭 신청 및 채팅방 참여 모델
class MatchingRequest(models.Model):
    STATUS_CHOICES = (
        ('PENDING', '대기 중'),
        ('ACCEPTED', '수락됨'),
        ('REJECTED', '거절됨'),
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='matching_requests')
    guest = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='my_requests')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'guest')  # 한 글에 중복 신청 방지


# 2. 채팅 메시지 모델 (댓글 달기와 똑같습니다!)
class ChatMessage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='chat_messages')
    
    # 💡 sender가 비어있으면(null) "OO님이 입장하셨습니다" 같은 시스템 메시지로 처리합니다.
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']  # 옛날 메시지부터 순서대로 정렬 (채팅창 흐름)