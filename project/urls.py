from django.contrib import admin
from django.urls import path, include

from main.views import RegisterUserView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('roteiro/v1/', include('main.urls', namespace='main')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-auth/register', RegisterUserView.as_view(), name='register')

]
