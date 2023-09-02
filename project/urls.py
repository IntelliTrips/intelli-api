from django.contrib import admin
from django.urls import path, include

from main.views import RegisterUserView, custom_login, get_csrf_token, custom_logout, check_session_validity

urlpatterns = [
    path('admin/', admin.site.urls),
    path('roteiro/v1/', include('main.urls', namespace='main')),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-auth/login/', custom_login, name='login'),
    path('api-auth/logout/', custom_logout, name='logout'),
    path('api-auth/register/', RegisterUserView.as_view(), name='register'),
    path('api-auth/session/check/', check_session_validity, name='check_session_validity'),
    path('csrf/', get_csrf_token, name='get_csrf_token')
]
