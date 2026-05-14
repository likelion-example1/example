from rest_framework import serializers

from .models import User

from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):

 class Meta:

    model = User

    fields = (

            'id', 'username', 'email', 'password'

        )
    
    extra_kwargs = {
            'password': {'write_only': True} 
        }
    
 def create(self, validated_data):

    user = User.objects.create(

        username=validated_data['username'],

        email=validated_data['email']

    )

    user.set_password(validated_data['password'])

    user.save()


    return user


class UserLoginSerializer(serializers.Serializer):

 email = serializers.CharField(max_length=100)

 password = serializers.CharField(max_length=128, write_only=True)
 
 
 def validate(self, data):

    email = data.get('email')

    password = data.get('password')


    if User.objects.filter(email=email).exists():

        user = User.objects.get(email=email)

 

        if not user.check_password(password):

            raise serializers.ValidationError()

        else:

            token = RefreshToken.for_user(user)

            refresh = str(token)

            access = str(token.access_token)


            return {

                 'id': user.id,

                'email': user.email,

                'access': access,

                'refresh': refresh

                }
    else:
            raise serializers.ValidationError("가입되지 않은 이메일입니다.")
            
            
            
            
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])

    # 기존 비밀번호가 맞는지 검사
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("기존 비밀번호가 틀렸습니다.")
        return value