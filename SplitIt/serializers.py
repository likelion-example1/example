from rest_framework import serializers

from .models import Post, Comment
from .models import MatchingRequest, ChatMessage

        
class CommentSerializer(serializers.ModelSerializer):
    class Meta:

        model = Comment

        fields = (

            'id', 'post', 'author', 'author_username', 'comment_text', 'created_at'
        )
        
class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    host_nickname = serializers.CharField(source='host.profile.nickname', read_only=True)
    class Meta:

        model = Post

        fields = (

            'id', 'title', 'date', 'body', 'language', 'comments', 
            'host', 'participants', 'photo',
            'location', 'category', 'status', 'pickup_time',
            'delivery_fee', 'min_order_amount',
            'host_nickname'

        )
        read_only_fields = ['host']
        
        
# 1. 채팅 메시지 전용 이름표
class ChatMessageSerializer(serializers.ModelSerializer):
    sender_nickname = serializers.CharField(source='sender.profile.nickname', read_only=True)
    is_system = serializers.SerializerMethodField()

    class Meta:
        model = ChatMessage
        fields = ('id', 'sender_nickname', 'content', 'created_at', 'is_system')

    def get_is_system(self, obj):
        return obj.sender is None  # 보낸 사람이 없으면 시스템 메시지(True)


# 2. 채팅방 목록 전용 이름표
class ChatRoomListSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    host_nickname = serializers.CharField(source='host.profile.nickname', read_only=True)
    last_message = serializers.SerializerMethodField()
    pending_count = serializers.SerializerMethodField()  # 빨간 알림 숫자
    status_display = serializers.SerializerMethodField() # '매칭 대기중' 등 표시용

    class Meta:
        model = Post
        fields = ('id', 'title', 'location', 'category', 'host_nickname', 'type', 'last_message', 'pending_count', 'status_display', 'min_order_amount')

    def get_type(self, obj):
        request = self.context.get('request')
        if obj.host == request.user:
            return 'received'  # 내가 받은 신청 (내가 호스트)
        return 'sent'          # 내가 보낸 신청 (내가 게스트)

    def get_last_message(self, obj):
        # 마지막 메시지 미리보기 (수락 안 됐으면 대화 미리보기 불가능 처리)
        request = self.context.get('request')
        if obj.host != request.user:
            my_req = MatchingRequest.objects.filter(post=obj, guest=request.user).first()
            if my_req and my_req.status == 'PENDING':
                return "대화 미리보기 불가능"
        
        last_msg = obj.chat_messages.last()
        return last_msg.content if last_msg else "아직 대화가 없습니다."

    def get_pending_count(self, obj):
        # 대기 중인 새로운 매칭 신청 수 (빨간 배지)
        return obj.matching_requests.filter(status='PENDING').count()

    def get_status_display(self, obj):
        request = self.context.get('request')
        if obj.host != request.user:
            my_req = MatchingRequest.objects.filter(post=obj, guest=request.user).first()
            if my_req and my_req.status == 'PENDING':
                return "매칭 대기중"
        return obj.status  # 원래 게시글의 상태 (매칭중 / 매칭완료 등)
    
    
class MatchingRequestSerializer(serializers.ModelSerializer):
    guest_id = serializers.IntegerField(source='guest.id', read_only=True)
    guest_nickname = serializers.CharField(source='guest.profile.nickname', read_only=True)
    guest_profile_image = serializers.SerializerMethodField()

    class Meta:
        model = MatchingRequest
        fields = ('guest_id', 'guest_nickname', 'guest_profile_image', 'status')

    def get_guest_profile_image(self, obj):
        request = self.context.get('request')
        profile = obj.guest.profile
       
        if profile.profile_image:
            return request.build_absolute_uri(profile.profile_image.url)
        return ""