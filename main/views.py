from django.shortcuts import get_object_or_404
from .serializers import RoteiroListSerializer, RoteiroSerializer, UserCreateSerializer
from .models import Roteiro
from rest_framework import viewsets, permissions, views
from rest_framework.response import Response


# ViewSet é uma classe que contém os métodos que serão utilizados na API
class RoteiroViewSet(viewsets.ModelViewSet):
    queryset = (
        Roteiro.objects.all()
    )  # queryset é uma variável que contém todos os objetos do banco de dados
    serializer_class = RoteiroSerializer  # serializer_class é uma variável que contém a classe que serializa os dados do banco de dados
    permission_classes = [
        permissions.IsAuthenticated
    ]  # permission_classes é uma variável que contém as permissões de acesso a API

    def list(self, request):
        queryset = self.queryset.filter(usuario=request.user)
        serializer = RoteiroListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        queryset = self.queryset.filter(usuario=request.user)
        roteiro = get_object_or_404(queryset, pk=pk)
        serializer = RoteiroListSerializer(roteiro)
        return Response(serializer.data)
    

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        roteiro = serializer.save()
        roteiro.usuario = request.user
        roteiro.save()
        serializer_com_todos_os_campos = RoteiroListSerializer(roteiro)
        return Response(serializer_com_todos_os_campos.data)


class RegisterUserView(views.APIView):
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "User created successfully"})
