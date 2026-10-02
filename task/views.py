from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *

# Create your views here.

class TaskModelViewSet(ModelViewSet):
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated,]
    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
