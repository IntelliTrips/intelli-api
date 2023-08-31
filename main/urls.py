from rest_framework.routers import DefaultRouter
from .views import RegisterUserView, RoteiroViewSet
from django.urls import path

# Responsável por criar as rotas da API e definir o nome da aplicação que será usado na URL da API (http:// localhost:8000/api/roteiros)
app_name = "api"
router = DefaultRouter(
    trailing_slash=False
)  # significa que não terá barra no final da URL
router.register(
    r"roteiros", RoteiroViewSet, basename="Roteiro"
)  # registra a rota para o viewset RoteiroViewSet

urlpatterns = [path("register/", RegisterUserView.as_view())]

urlpatterns += router.urls  # define as rotas da API
