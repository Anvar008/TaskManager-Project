import datetime

from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import *
from .serializers import *
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.views import APIView

# Create your views here.

class ProjectCreateAPIView(CreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializers
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [JWTAuthentication, ]

    def post(self, request, *args, **kwargs):
        serializer = ProjectSerializers(data=self.request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(owner=request.user)
            return Response({
                'message': 'OK',
                'status': 201,
                'data': serializer.data
            })

class ProjectListAPIView(ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectListSerializers
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        user = request.user
        projects = Project.objects.filter(owner=user.id)
        serializer = ProjectListSerializers(projects, many=True)
        return Response({
            'message': 'OK',
            'status': 200,
            'data': serializer.data
        })


class ProjectAddMemberAPIView(CreateAPIView):
    queryset = Project
    serializer_class = ProjectAddMemberSerializers
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user=request.user
        project_id = kwargs['pk']
        project = Project.objects.filter(owner=user.id, id=project_id).first()
        if not project:
            return Response({
                'message': 'You dont have that project',
                'status': 400
            })
        req_user = request.data['user']
        check_user = ProjectMember.objects.filter(
            project=project_id,
            user=req_user
        ).exists()
        if check_user:
            return Response({
                'message': 'You already add that user',
                'status': 200
            })
        serializer = ProjectAddMemberSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            date = datetime.date.today()
            print(date)
            serializer.save(project=project, join_date=date)
            return Response({
                'message': 'OK',
                'status': '200',
                'data': serializer.data
            })
        return Response({
            'message': 'Smth went wrong',
            'status': 400
        })
