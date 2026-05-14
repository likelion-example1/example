from django.urls import path

from .views import *


app_name = 'accounts'


urlpatterns = [

 path('signup/', SignUpView.as_view()),
 path('login/', LoginView.as_view()),
 path('logout/', LogoutView.as_view(), name='logout'),
 path('profile/', ProfileView.as_view(), name='profile'),
 path('password-change/', ChangePasswordView.as_view(), name='password_change'),
 ]