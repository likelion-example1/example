# Create your views here.
from django.http import HttpRequest, Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post
from .serializers import PostSerializer, CommentSerializer


class PostListView(APIView):

    def get(self, request:HttpRequest, format=None):

        posts = Post.objects.all()

        serializer = PostSerializer(posts, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request:HttpRequest, format=None):

        serializer = PostSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

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