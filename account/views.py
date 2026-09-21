from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import *

# Create your views here.

class RegisterAPIView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer


class LoginApiView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = LoginSerializers

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token

            return Response({
                'message': 'Ok',
                'status': 200,
                'access': str(access),
                'refresh': str(refresh)
            })
        else:
            return Response('Invalid')
