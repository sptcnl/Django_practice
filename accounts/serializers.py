from rest_framework import serializers, status
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
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


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
                                    required=True, 
                                    write_only=True
                                )
    new_password = serializers.CharField(
                                    required=True, 
                                    write_only=True, 
                                    validators=[validate_password]
                                )

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                '이전 비밀번호가 유효하지 않습니다. 다시 시도해주세요.'
            )
        return value

    def validate(self, data):
        if data['old_password'] == data['new_password']:
            raise serializers.ValidationError(
                {'error': '새 비밀번호는 이전 비밀번호와 동일하지 않아야합니다.'}
                )
        return data

    def save(self, **kwarg):
        password = self.validated_data['new_password']
        user = self.context['request'].user
        user.set_password(password)
        user.save()
        return 


class ProfileSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150, 
        required=False,
        validators=[UniqueValidator(queryset=User.objects.all())]
        )
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    gender = serializers.ChoiceField(choices=(
                                ('M', 'Man'),
                                ('W', 'Woman'),
                                ('O', 'Other'),
                                ),
                                required=False)
    profile_picture = serializers.ImageField(required=False)
    bio = serializers.CharField(required=False)
    birth = serializers.DateField(required=False)

    def create(self, validated_data):

        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        return instance