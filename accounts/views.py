from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from accounts.serializers import SignupSerializer, LoginSerializer

@api_view(['POST'])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

def login(request, how):
    print(how)
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    if how == 'token':
        token = serializer.validated_data
        return Response({"token": token.key}, status=status.HTTP_200_OK)