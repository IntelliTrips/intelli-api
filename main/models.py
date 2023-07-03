from django.db import models

class Roteiro(models.Model):
    destino = models.CharField(max_length=100)
    data_ida = models.CharField(null=True, blank=True, max_length=12)
    data_volta = models.CharField(null=True, blank=True, max_length=12)
    quantidade_pessoas = models.IntegerField()