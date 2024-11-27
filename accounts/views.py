from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from accounts.serializers import SignupSerializer

@api_view(['POST'])
def signup(request):
    serializer = SignupSerializer(data = request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)