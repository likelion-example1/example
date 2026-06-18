from rest_framework import serializers

from .models import User, Profile

from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=150)         # 프론트의 로그인 아이디
    pw = serializers.CharField(write_only=True)        # 프론트의 비밀번호
    username = serializers.CharField(max_length=50)    # 프론트의 닉네임 (User Name)
    
    def create(self, validated_data):
        # 2. 프론트가 보낸 'id' 값을 장고의 로그인 아이디(username) 칸에 쏙 넣어서 유저를 만듭니다.
        user = User.objects.create(
            username=validated_data['id'] 
        )
        
        # 3. 프론트가 보낸 'pw' 값으로 비밀번호를 암호화해서 세팅합니다.
        user.set_password(validated_data['pw'])
        user.save()

        # 4. 프론트가 보낸 'username' 값은 Profile의 'nickname' 칸에 예쁘게 저장합니다!
        Profile.objects.create(user=user, nickname=validated_data['username'])

        return user
    
    # (선택) 회원가입 성공 후 프론트엔드에게 응답(Response)으로 보여줄 데이터 모양
    def to_representation(self, instance):
        return {
            "id": instance.username,                # 가입된 로그인 아이디 반환
            "username": instance.profile.nickname,  # 가입된 닉네임 반환
            "message": "회원가입이 성공적으로 완료되었습니다!"
        }

 


class UserLoginSerializer(serializers.Serializer):

 username = serializers.CharField(max_length=150)

 password = serializers.CharField(max_length=128, write_only=True)
 
 
 def validate(self, data):

    username = data.get('username')

    password = data.get('password')


    if User.objects.filter(username=username).exists():

        user = User.objects.get(username=username)

 

        if not user.check_password(password):

            raise serializers.ValidationError("비밀번호가 틀렸습니다.")

        else:

            token = RefreshToken.for_user(user)

            refresh = str(token)

            access = str(token.access_token)


            return {

                 

                'username': user.username,
                
                'nickname': user.profile.nickname if hasattr(user, 'profile') else "",

                'access': access,

                'refresh': refresh

                }
    else:
            raise serializers.ValidationError("가입되지 않은 아이디입니다.")
            
            
            
            
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])

    # 기존 비밀번호가 맞는지 검사
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("기존 비밀번호가 틀렸습니다.")
        return value
    
    
class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('nickname', 'profile_image') # 프론트엔드한테 닉네임만 딱 받아서 수정하겠다는 뜻