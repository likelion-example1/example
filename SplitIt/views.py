# Create your views here.
from django.http import HttpRequest, Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post
from .serializers import PostSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from django.db.models import Q
from .models import MatchingRequest, ChatMessage
from .serializers import ChatRoomListSerializer, ChatMessageSerializer, MatchingRequestSerializer

class PostListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request:HttpRequest, format=None):

        posts = Post.objects.all()

        search_location = request.GET.get('location')
        search_category = request.GET.get('category')
        search_keyword = request.GET.get('keyword')

        if search_location:
            posts = posts.filter(location=search_location)
            
        if search_category:
            posts = posts.filter(category=search_category)
            
        if search_keyword:
            posts = posts.filter(
                Q(title__icontains=search_keyword) | Q(body__icontains=search_keyword)
            )


        serializer = PostSerializer(posts, many=True, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request:HttpRequest, format=None):

        serializer = PostSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save(host=request.user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class PostDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404


    def get(self, request:HttpRequest, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    def put(self, request:HttpRequest, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post, data=request.data, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request:HttpRequest, pk, format=None):

        post = self.get_object(pk)

        post.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
    
class CommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request:HttpRequest, format=None):

        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save(author=request.user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class MyPostListView(APIView):
    permission_classes = [IsAuthenticated] # 로그인한 사람만 접근 가능

    def get(self, request):
       
        user_posts = Post.objects.filter(host=request.user)
        
        serializer = PostSerializer(user_posts, many=True, context={'request': request})
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    
class MyMatchingHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 1. 내가 작성한 게시물
        requested_matches = Post.objects.filter(host=request.user)
        
        # 2. 내가 수락한 게시물
        accepted_matches = Post.objects.filter(participants=request.user)

        requested_serializer = PostSerializer(requested_matches, many=True, context={'request': request})
        accepted_serializer = PostSerializer(accepted_matches, many=True, context={'request': request})
       
        return Response({
            "requested_matches": requested_serializer.data,
            "accepted_matches": accepted_serializer.data
        }, status=status.HTTP_200_OK)
        
        
        
class JoinPostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        
        post = get_object_or_404(Post, id=post_id)
        user = request.user

        # 본인글
        if post.host == user:
            return Response({"message": "본인이 작성한 글에는 참여할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

        # 이미 참여중
        if post.participants.filter(id=user.id).exists() or MatchingRequest.objects.filter(post=post, guest=user).exists():
            
            return Response({"message": "이미 참여 중인 게시글입니다."}, status=status.HTTP_400_BAD_REQUEST)

        MatchingRequest.objects.create(
            post=post,
            guest=user,
            status='PENDING'
        )
             
        return Response({"message": "매칭 신청이 완료되었습니다. 방장의 수락을 기다려주세요!"}, status=status.HTTP_200_OK)
    
    
    # 1. 채팅방 목록 조회 (GET /chats/)
class ChatRoomListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 내가 호스트이거나, 내가 게스트로 신청한 모든 게시글(채팅방)을 가져옵니다.
        posts = Post.objects.filter(
            Q(host=request.user) | Q(matching_requests__guest=request.user)
        ).distinct()

        # 지난 매칭 숨기기 필터링 (isPastHidden)
        is_past_hidden = request.GET.get('isPastHidden', 'false') == 'true'
        if is_past_hidden:
            posts = posts.exclude(status='매칭완료') # 본인의 '완료' 상태 텍스트에 맞게 수정하세요!

        serializer = ChatRoomListSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


# 2. 세부 채팅방 메시지 확인 및 전송 (/chats/<post_id>/messages/)
class ChatMessageView(APIView):
    permission_classes = [IsAuthenticated]

    # 메시지 내역 가져오기 (프론트가 3초마다 이거를 계속 호출(Polling)할 겁니다!)
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        messages = post.chat_messages.all()
        serializer = ChatMessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 메시지 보내기
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        content = request.data.get('content')
        
        if not content:
            return Response({"message": "내용을 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)

        message = ChatMessage.objects.create(
            post=post,
            sender=request.user,
            content=content
        )
        serializer = ChatMessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# 3. 호스트가 매칭 신청을 수락하거나 거절하는 API (/chats/<post_id>/respond/)
class MatchRespondView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        guest_id = request.data.get('request_id') # 프론트가 수락/거절할 유저 ID를 보내줌
        action = request.data.get('action')     # 'accept' 또는 'reject'

        if post.host != request.user:
            return Response({"message": "방장만 수락/거절할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)

        req = get_object_or_404(MatchingRequest, id=request_id, post=post)

        if action == 'accept':
            req.status = 'ACCEPTED'
            req.save()
            post.participants.add(req.guest) # 참여자 명단에 추가

            # 💡 핵심: 시스템 메시지를 자동으로 하나 쏘아 올립니다!
            ChatMessage.objects.create(
                post=post,
                sender=None, # System
                content=f"{req.guest.profile.nickname} 님이 입장하셨습니다."
            )
            return Response({"message": "매칭 신청을 수락했습니다."}, status=status.HTTP_200_OK)

        elif action == 'reject':
            req.status = 'REJECTED'
            req.save()
            return Response({"message": "매칭 신청을 거절했습니다."}, status=status.HTTP_200_OK)

        return Response({"message": "잘못된 요청입니다."}, status=status.HTTP_400_BAD_REQUEST)
    
    
class MatchRequestListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)

        # 1. 방장(호스트)이 아니면 빈 배열을 주거나 권한 없다고 튕겨냅니다.
        if post.host != request.user:
            return Response([], status=status.HTTP_200_OK)

        # 2. 이 방에 신청한 사람 중, 상태가 'PENDING(대기 중)'인 사람만 필터링!
        pending_requests = MatchingRequest.objects.filter(post=post, status='PENDING')
        
       
        serializer = MatchingRequestSerializer(pending_requests, many=True, context={'request': request})
        
        return Response(serializer.data, status=status.HTTP_200_OK)