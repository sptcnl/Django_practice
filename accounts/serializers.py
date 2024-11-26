from rest_framework import serializers
from accounts.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 
            'first_name',
            'last_name',
            'email', 
            'gender', 
            'profile_picture', 
            'bio', 
            'birth',
        )