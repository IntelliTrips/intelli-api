from django.db import models
from django.contrib.auth import get_user_model

# Modelo de roteiro salvo no banco de dados
class Roteiro(models.Model):
    destino = models.CharField(max_length=100)
    data_ida = models.CharField(null=True, blank=True, max_length=12)
    data_volta = models.CharField(null=True, blank=True, max_length=12)
    quantidade_pessoas = models.IntegerField()
    texto_usuario = models.TextField(default="")
    resposta_chatgpt = models.TextField(default="")

    def __str__(self):
        return self.destino
