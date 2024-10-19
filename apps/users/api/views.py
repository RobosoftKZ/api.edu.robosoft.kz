from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.users.models import User
from .serializers import UserSerializer, UsernameSerializer


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class UsernameCheckerAPIView(APIView):
    serializer_class = UsernameSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        # Получаем имя пользователя из запроса
        username = request.data.get("username")

        # Проверяем, было ли передано имя пользователя
        if not username:
            return Response({"error": "Username is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Проверяем, существует ли пользователь с таким именем
        if User.objects.filter(username=username).exists():
            return Response({"available": False}, status=status.HTTP_200_OK)
        else:
            return Response({"available": True}, status=status.HTTP_200_OK)


class LoginRegisterAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            # Check if user exists
            user = authenticate(username=username, password=password)
            if user:
                # If user exists and is authenticated, return their token
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'message': 'Login successful', 'token': token.key}, status=status.HTTP_200_OK)

            else:
                # If user does not exist, register a new user
                if not User.objects.filter(username=username).exists():
                    # Create new user
                    user = User.objects.create_user(username=username, password=password)
                    token, _ = Token.objects.get_or_create(user=user)
                    return Response({'message': 'Registration successful', 'token': token.key},
                                    status=status.HTTP_201_CREATED)
                else:
                    # Incorrect password for an existing user
                    return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
