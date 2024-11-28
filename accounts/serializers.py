from rest_framework import serializers, status
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

User = get_user_model()

class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150, 
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
        )
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    gender = serializers.ChoiceField(choices=(
                                ('M', 'Man'),
                                ('W', 'Woman'),
                                ('O', 'Other'),
                                )
                            )
    profile_picture = serializers.ImageField(required=False)
    bio = serializers.CharField(required=False)
    birth = serializers.DateField(required=False)
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
    )
    password2 = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {'password': '비밀번호가 일치하지 않습니다.'}
            )
        return data
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username = validated_data['username'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            email = validated_data['email'],
            gender = validated_data['gender'],
            profile_picture = validated_data['profile_picture'],
            bio = validated_data['bio'],
            birth = validated_data['birth'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


# class LoginSerializer(serializers.Serializer):
#     username = serializers.CharField(required=True)
#     password = serializers.CharField(required=True, write_only=True)

#     def validate(self, data):
#         user = authenticate(**data)
#         if user:
#             # 아직 view에서 serializer로 how 넘기는거 추가 안함
#             refresh = RefreshToken.for_user(user)
#             return Response({'refresh_token': str(refresh),
#                             'access_token': str(refresh.access_token)}, status=status.HTTP_200_OK)
#         raise serializers.ValidationError(
#             {"error": "계정이 유효하지 않음"}
#         )