from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .serializers import RoteiroListSerializer, RoteiroSerializer, UserCreateSerializer
from .models import Roteiro
from rest_framework import viewsets, permissions, views
from rest_framework.response import Response
from django.middleware.csrf import get_token
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from django.contrib.sessions.models import Session
from django.utils import timezone


# ViewSet é uma classe que contém os métodos que serão utilizados na API
class RoteiroViewSet(viewsets.ModelViewSet):
    queryset = (
        Roteiro.objects.all()
    )  # queryset é uma variável que contém todos os objetos do banco de dados
    # serializer_class é uma variável que contém a classe que serializa os dados do banco de dados
    serializer_class = RoteiroSerializer
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


@api_view(['POST'])
@permission_classes([])
def custom_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Login failed'}, status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['POST'])
@permission_classes([])
def custom_logout(request):
    logout(request)
    return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)


def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken': csrf_token})


def check_session_validity(request):
    session_key = request.session.session_key
    try:
        session = Session.objects.get(session_key=session_key)
        if session.expire_date > timezone.now():
            return JsonResponse({'valid': True, 'sessionId': session_key}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'valid': False, 'sessionId': session_key}, status=status.HTTP_401_UNAUTHORIZED)
    except Session.DoesNotExist:
        return JsonResponse({'valid': False , 'sessionId': session_key}, status=status.HTTP_401_UNAUTHORIZED)
