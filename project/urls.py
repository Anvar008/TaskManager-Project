from django.urls import path
from .views import *

urlpatterns = [
    path('project/create/', ProjectCreateAPIView.as_view()),
    path('project/list/', ProjectListAPIView.as_view()),
    path('project/<int:pk>/add/member/', ProjectAddMemberAPIView.as_view()),
]
