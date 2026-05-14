from django.urls import path

from .views import *

from .views import PostListView, MyPostListView

app_name = 'SplitIt'


urlpatterns = [

 path('', PostListView.as_view()),
 path('<int:pk>/', PostDetailView.as_view()),
 path('comments/', CommentView.as_view()),
 path('', PostListView.as_view(), name='post_list'),
 path('my-posts/', MyPostListView.as_view(), name='my_posts'),
 path('matching-history/', MyMatchingHistoryView.as_view(), name='matching_history'),
 path('<int:post_id>/join/', JoinPostView.as_view(), name='join_post'),

]