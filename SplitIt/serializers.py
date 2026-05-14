from rest_framework import serializers

from .models import Post, Comment

        
class CommentSerializer(serializers.ModelSerializer):
    class Meta:

        model = Comment

        fields = (

            'id', 'post', 'username', 'comment_text', 'created_at'
        )
        
class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:

        model = Post

        fields = (

            'id', 'title', 'date', 'body', 'language', 'comments', 'host', 'participants', 'photo'

        )
        read_only_fields = ['host']