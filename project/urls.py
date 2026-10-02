from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import *

# urlpatterns = [
    # path('project/create/', ProjectCreateAPIView.as_view()),
    # path('project/list/', ProjectListAPIView.as_view()),
    # path('project/<int:pk>/add/member/', ProjectAddMemberAPIView.as_view()),
# ]


router = DefaultRouter()
router.register('project', ProjectViewSet, basename='project')

urlpatterns = router.urls
