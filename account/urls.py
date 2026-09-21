from django.urls import path
from .models import *
from .views import RegisterAPIView, LoginApiView

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('login/', LoginApiView.as_view()),
]
