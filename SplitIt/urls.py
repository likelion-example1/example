from django.urls import path

from .views import *

from .views import PostListView, MyPostListView

app_name = 'SplitIt'


urlpatterns = [

    path('posts/', PostListView.as_view(), name='post_list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('posts/comments/', CommentView.as_view(), name='comments'),
    path('posts/my-posts/', MyPostListView.as_view(), name='my_posts'),
    path('posts/matching-history/', MyMatchingHistoryView.as_view(), name='matching_history'),
    path('posts/<int:post_id>/join/', JoinPostView.as_view(), name='join_post'),
]