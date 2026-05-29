from rest_framework import serializers

from .models import Post, Comment

        
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
            'location', 'category', 'status', 'pickup_time'
            'delivery_fee', 'min_order_amount'

        )
        read_only_fields = ['host']