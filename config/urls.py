from rest_framework import permissions

from drf_yasg.views import get_schema_view

from drf_yasg import openapi
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

schema_view = get_schema_view(

    openapi.Info(

        title="My API",

        default_version='v1',

        description="Test description",

    ),

    public=True,

    permission_classes=[permissions.AllowAny, ],
    authentication_classes=[],
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger',
    cache_timeout=0), name='schema-swagger-ui'),

        path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
    name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('api/v1/', include([
        path('', include('account.urls')),
        path('', include('project.urls')),
        path('', include('task.urls')),
        path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    ])),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
