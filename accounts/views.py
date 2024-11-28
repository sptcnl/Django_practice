from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.serializers import SignupSerializer
from django.contrib.auth import (
                                login as session_login,
                                logout as session_logout,
                                )

@api_view(['POST'])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def login(request, how):
    login_ways = ['token', 'session']
    if how not in login_ways:
        return Response({'error': how + '의 url은 지원하고 있지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
    
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'message': '아이디 또는 비밀번호가 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
    
    if how == 'token':
        refresh = RefreshToken.for_user(user)
        return Response({'refresh_token': str(refresh),
                        'access_token': str(refresh.access_token)}, status=status.HTTP_200_OK)
    elif how == 'session':
        session_login(request, user)
        return Response({'message': '세션 로그인 성공'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request, how):
    login_ways = ['token', 'session']
    if how not in login_ways:
        return Response({'error': how + '의 url은 지원하고 있지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
    
    if how == 'token':
        refresh = request.data.get("refresh")
        if not refresh:
            return Response({"message": "refresh token 필요"}, status=status.HTTP_400_BAD_REQUEST)
        token = RefreshToken(refresh)
        token.blacklist()
        return Response({'message': '토큰 로그아웃 성공'}, status=status.HTTP_200_OK)
    elif how == 'session':
        session_logout(request)
        return Response({'message': '세션 로그아웃 성공'}, status=status.HTTP_200_OK)