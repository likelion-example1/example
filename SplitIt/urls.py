from django.urls import path

from .views import *


app_name = 'SplitIt'


urlpatterns = [

 path('', PostListView.as_view()),
 path('<int:pk>/', PostDetailView.as_view()),
 path('comments/', CommentView.as_view()),

]