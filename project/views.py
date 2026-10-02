# import datetime
#
# from django.shortcuts import render
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework_simplejwt.authentication import JWTAuthentication
#
# from .models import *
# from .serializers import *
# from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
# from rest_framework.views import APIView
#
# # Create your views here.
#
# class ProjectCreateAPIView(CreateAPIView):
#     queryset = Project.objects.all()
#     serializer_class = ProjectSerializers
#     permission_classes = [IsAuthenticated, ]
#     authentication_classes = [JWTAuthentication, ]
#
#     def post(self, request, *args, **kwargs):
#         serializer = ProjectSerializers(data=self.request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save(owner=request.user)
#             return Response({
#                 'message': 'OK',
#                 'status': 201,
#                 'data': serializer.data
#             })
#
# class ProjectListAPIView(ListAPIView):
#     queryset = Project.objects.all()
#     serializer_class = ProjectListSerializers
#     permission_classes = [IsAuthenticated, ]
#
#     def get(self, request, *args, **kwargs):
#         user = request.user
#         projects = Project.objects.filter(owner=user.id)
#         serializer = ProjectListSerializers(projects, many=True)
#         return Response({
#             'message': 'OK',
#             'status': 200,
#             'data': serializer.data
#         })
#
#
# class ProjectAddMemberAPIView(CreateAPIView):
#     queryset = Project
#     serializer_class = ProjectAddMemberSerializers
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request, *args, **kwargs):
#         user=request.user
#         project_id = kwargs['pk']
#         project = Project.objects.filter(owner=user.id, id=project_id).first()
#         if not project:
#             return Response({
#                 'message': 'You dont have that project',
#                 'status': 400
#             })
#         req_user = request.data['user']
#         check_user = ProjectMember.objects.filter(
#             project=project_id,
#             user=req_user
#         ).exists()
#         if check_user:
#             return Response({
#                 'message': 'You already add that user',
#                 'status': 200
#             })
#         serializer = ProjectAddMemberSerializers(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             date = datetime.date.today()
#             print(date)
#             serializer.save(project=project, join_date=date)
#             return Response({
#                 'message': 'OK',
#                 'status': '200',
#                 'data': serializer.data
#             })
#         return Response({
#             'message': 'Smth went wrong',
#             'status': 400
#         })
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Q
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from account.models import CustomUser
from project.models import Project, ProjectMember
from project.permissions import IsProjectOwnerOrReadOnly
from project.serializers import (
    ProjectListSerializer,
    ProjectMemberIdsSerializer,
    ProjectMemberSerializer,
    ProjectSerializer,
)


class ProjectViewSet(viewsets.ModelViewSet):
    search_fields = ['name', ]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'description']
    # permission_classes = [IsAuthenticated, IsProjectOwnerOrReadOnly]

    # def get_queryset(self):
    #     user = self.request.user
    #     return (
    #         Project.objects
    #         .filter(Q(owner=user) | Q(members=user) | Q(visibility=Project.Visibility.PUBLIC))
    #         .distinct()
    #         .prefetch_related('members')    # list'da members uchun N+1 yo'q
    #     )

    def get_queryset(self):
        search_query = self.request.query_params.get('search')
        queryset = Project.objects.all()
        if search_query:
            queryset = queryset.annotate(
                similarity=TrigramSimilarity('name', search_query)
            ).filter(similarity__gt=0.2).order_by('-similarity')
        return queryset

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return ProjectListSerializer
        return ProjectSerializer

    def perform_create(self, serializer):
        # Faqat Project yaratiladi. ProjectMember bu yerda YARATILMAYDI.
        serializer.save(owner=self.request.user)

    # ---------- /projects/{id}/members/ ----------

    def _validated_users(self, project):
        ser = ProjectMemberIdsSerializer(
            data=self.request.data, context={'project': project},
        )
        ser.is_valid(raise_exception=True)
        return ser.validated_data['users']

    def _members_response(self, project):
        qs = project.project_members.order_by('created_at')
        return Response(ProjectMemberSerializer(qs, many=True).data)

    @action(detail=True, methods=['get'], url_path='members')
    def members(self, request, pk=None):
        """GET: a'zolar ro'yxati. get_object() 404 (ko'rinmaydi) yoki 403 (owner emas) beradi."""
        return self._members_response(self.get_object())

    @members.mapping.post
    def add_members(self, request, pk=None):
        """POST {"users": [2, 3]}: faqat owner."""
        project = self.get_object()
        users = self._validated_users(project)
        # >>> ProjectMember qatorlari AYNAN SHU YERDA yaratiladi <<<
        # Django ichida: mavjud user_id'lar SELECT, qolganlar uchun
        # ProjectMember(project=project, user=u, **through_defaults) bulk_create.
        project.members.add(
            *users,
            through_defaults={
                'role': ProjectMember.Role.MEMBER,
                'join_date': timezone.localdate(),   # USE_TZ=True; aks holda timezone.now().date()
            },
        )
        return self._members_response(project)

    @members.mapping.delete
    def remove_members(self, request, pk=None):
        """DELETE {"users": [2]}: faqat owner. A'zo bo'lmagan user jimgina o'tadi."""
        project = self.get_object()
        users = self._validated_users(project)
        project.members.remove(*users)   # ProjectMember.filter(project, user_id__in=...).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

