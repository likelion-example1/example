# Create your views here.
from django.http import HttpRequest, Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post
from .serializers import PostSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404

class PostListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request:HttpRequest, format=None):

        posts = Post.objects.all()

        search_location = request.GET.get('location')
        search_category = request.GET.get('category')

        if search_location:
            posts = posts.filter(location=search_location)
            
        if search_category:
            posts = posts.filter(category=search_category)


        serializer = PostSerializer(posts, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request:HttpRequest, format=None):

        serializer = PostSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save(host=request.user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class PostDetailView(APIView):

    def get_object(self, pk):

        try:

            return Post.objects.get(pk=pk)

        except Post.DoesNotExist:

            raise Http404


    def get(self, request:HttpRequest, pk, format=None):

        post = self.get_object(pk)

        serializer = PostSerializer(post)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    def put(self, request:HttpRequest, pk, format=None):

        post = self.get_object(pk)

        serializer = PostSerializer(post, data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request:HttpRequest, pk, format=None):

        post = self.get_object(pk)

        post.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
    
class CommentView(APIView):

    def post(self, request:HttpRequest, format=None):

        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class MyPostListView(APIView):
    permission_classes = [IsAuthenticated] # 로그인한 사람만 접근 가능

    def get(self, request):
       
        user_posts = Post.objects.filter(host=request.user)
        
        serializer = PostSerializer(user_posts, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    
class MyMatchingHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 1. 내가 작성한 게시물
        requested_matches = Post.objects.filter(host=request.user)
        
        # 2. 내가 수락한 게시물
        accepted_matches = Post.objects.filter(participants=request.user)

        requested_serializer = PostSerializer(requested_matches, many=True)
        accepted_serializer = PostSerializer(accepted_matches, many=True)

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
        if post.participants.filter(id=user.id).exists():
            
            return Response({"message": "이미 참여 중인 게시글입니다."}, status=status.HTTP_400_BAD_REQUEST)

        # 모집 인원 체크
        if post.participants.count() >= post.target_headcount:
             return Response({"message": "이미 모집 인원이 가득 찼습니다."}, status=status.HTTP_400_BAD_REQUEST)

        # 참여자 명단에 본인 추가
        post.participants.add(user)
        
        return Response({"message": "참여가 완료되었습니다!"}, status=status.HTTP_200_OK)