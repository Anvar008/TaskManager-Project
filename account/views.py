from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from .serializers import *

# Create your views here.

class RegisterAPIView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
