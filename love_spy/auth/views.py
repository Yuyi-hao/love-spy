from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_views, permission_classes
from rest_framework.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer
from .models import User



def register_user(request):
    if request.method == "POST":
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


def user_login(request):
    if request.method=='POST':
        username = request.data.get('username')
        password = request.data.get('password')

    try:
        user = authenticate(username=username, password=password)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
    return Response({'error': 'invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@permission_classes([IsAuthenticated])
def user_logout(request):
    if request.method=='POST':
        try:
            request.user.auth_token.delete()
            return Response({'message': 'Logged out'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": f'{e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
