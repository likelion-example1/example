# Create your views here.
from django.shortcuts import render
from django.http import HttpRequest

from rest_framework import status

from rest_framework.response import Response

from rest_framework.views import APIView

from .serializers import UserSerializer,  UserLoginSerializer

from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserSerializer, UserLoginSerializer, ChangePasswordSerializer


class SignUpView(APIView):

 def post(self, request:HttpRequest, format=None):

    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():

        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):

 def post(self, request:HttpRequest, format=None):

    serializer = UserLoginSerializer(data=request.data)

    if serializer.is_valid():

        return Response(serializer.validated_data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    # 로그아웃도 로그인한 사람만 할 수 있어야 하니까 권한 설정!
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # 유저가 보낸 데이터에서 'refresh' 토큰을 꺼냄
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            
            # 토큰을 블랙리스트에 추가하여 폐기
            token.blacklist()

            return Response({"message": "성공적으로 로그아웃 되었습니다."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            print("진짜 에러 원인:", e)
            return Response({"message": "잘못된 토큰이거나 이미 로그아웃 되었습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        
        
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
       
        user = request.user
        return Response({
            
            "username": user.username,
            "id": user.id,
           
        }, status=status.HTTP_200_OK)
        
    def patch(self, request):
        user = request.user
        return Response({"message": "프로필 수정 API 준비 완료!"}, status=status.HTTP_200_OK)
        
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            # 새 비밀번호를 암호화해서 저장
            request.user.set_password(serializer.validated_data['new_password'])
            request.user.save()
            return Response({"message": "비밀번호가 성공적으로 변경되었습니다."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)