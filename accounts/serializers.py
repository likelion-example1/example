from rest_framework import serializers

from .models import User

from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):

 class Meta:

    model = User

    fields = (

            'id', 'username', 'password'

        )
    
    extra_kwargs = {
            'password': {'write_only': True} 
        }
    
 def create(self, validated_data):

    user = User.objects.create(

        username=validated_data['username'],
        

        

    )

    user.set_password(validated_data['password'])

    user.save()


    return user


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

                 'id': user.id,

                'username': user.username,

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