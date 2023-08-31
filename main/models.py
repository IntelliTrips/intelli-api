from django.db import models
import openai
import os
import json

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.Model.list()
from .utils import CIDADES


# Modelo de roteiro salvo no banco de dados
class Roteiro(models.Model):
    partida = models.CharField(
        max_length=100, choices=CIDADES, null=False, blank=False, default="Partida"
    )
    destino = models.CharField(
        max_length=100, choices=CIDADES, null=False, blank=False, default="Destino"
    )
    data_ida = models.DateField(null=False, blank=False)
    data_volta = models.DateField(null=False, blank=False)
    quantidade_pessoas = models.IntegerField(null=False, blank=False)
    custo = models.FloatField(null=False, blank=False, default=0)
    texto_usuario = models.TextField(null=True, blank=True)
    resposta_chatgpt = models.TextField(null=True, blank=True)
    data_requisicao = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, null=True, blank=True
    )

    def gerar_resposta(self, texto):
        MODEL = "gpt-3.5-turbo"
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "Você é um assistente de viagem muito experiente e responsável por montar um roteiro de viagem, considerando os pontos turísticos do destino, de acordo com os requisitos do usuário em termos de custo, local de partida, destino, período e quantidade de pessoas. A resposta deverá ser um JSON com os campos: partida, destino, orcamento, pessoas e roteiro. O roteiro é uma lista de objetos com os seguintes campos: data, hora, lugar, atividade, descricao, custo. Lembre-se de detalhar a descricao da atividade.",
                },
                {
                    "role": "user",
                    "content": texto,
                },
            ],
            # messages2=[
            #     {
            #         "role": "system",
            #         "content": "Você é um assistente de viagem muito experiente e responsável por montar um roteiro de viagem, considerando os pontos turísticos dos destino, de acordo com os requisitos do usuário em termos de custo, local de partida, destino, período e quantidade de pessoas. A resposta deverá ser um JSON com uma lista de objetos cada um com os seguintes campos: data e hora, lugar, atividade, custo",
            #     },
            #     {"role": "user", "content": texto},
            # ],
            temperature=0.7,
        )
        return response["choices"][0]["message"]["content"]

    def save(self, *args, **kwargs):
        self.texto_usuario = f"Requisitos: Custo: R${self.custo}, local de partida: {self.partida}, quantidade de pessoas: {self.quantidade_pessoas}, Destino: {self.destino}, período: de {self.data_ida} até {self.data_volta}."
        self.resposta_chatgpt = json.loads(self.gerar_resposta(self.texto_usuario))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.destino
