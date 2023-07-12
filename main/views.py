from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from .forms import RoteiroForm
from .models import Roteiro
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.Model.list()

# Função para gerar a resposta do chatgpt
def gerar_resposta(texto):
    resposta = openai.Completion.create(
        engine="text-davinci-003",
        prompt=texto,
        max_tokens=1500,
        temperature=0.7,
        n=1,
        stop=None,
    )
    return resposta.choices[0].text.strip()

# Função para criar um novo roteiro
def newRoteiroView(request):
    resposta_chatgpt = None  # Definindo inicialmente como None
    if request.method == "POST":
        form = RoteiroForm(request.POST)
        if form.is_valid(): # Se o formulário for válido, pega os dados do formulário e salva no banco de dados
            destino = form.cleaned_data["destino"]
            data_ida = form.cleaned_data["data_ida"]
            data_volta = form.cleaned_data["data_volta"]
            quantidade_pessoas = form.cleaned_data["quantidade_pessoas"]

            texto_usuario = f"Faça um roteiro de viagem para {destino}. Na data de {data_ida} à {data_volta}. Com {quantidade_pessoas} pessoas. Separe por tabela: Dia, turno,atividade e custo as sugestoes."

            resposta_chatgpt = gerar_resposta(texto_usuario)
            roteiro = Roteiro.objects.create(
                destino=destino,
                data_ida=data_ida,
                data_volta=data_volta,
                quantidade_pessoas=quantidade_pessoas,
                texto_usuario=texto_usuario,
                resposta_chatgpt=resposta_chatgpt,
            )
            roteiro.save()
            messages.success(request, "Roteiro concluido.")
            return render(
                request, "main/cadastro-roteiro.html", {"resposta": resposta_chatgpt} # Renderiza o template com a resposta do chatgpt
            )
    else:
        form = RoteiroForm() # Se não for POST, cria um formulário vazio
    return render(
        request,
        "main/cadastro-roteiro.html",
        {"form": form, "resposta": resposta_chatgpt}, # Renderiza o template com o formulário vazio
    )


# Função para listar todos os roteiros
def roteirosView(request):
    roteiros = Roteiro.objects.all() # Pega todos os roteiros do banco de dados
    return render(request, "main/roteiros.html", {"roteiros": roteiros})

# Função para listar um roteiro específico
def roteirosIdView(request, id):
    roteiro = get_object_or_404(Roteiro, pk=id) # Pega o roteiro com o id passado na url
    return render(request, "main/roteiro.html", {"roteiro": roteiro}) 


# Função para deletar um roteiro
def deleteRoteiro(request, id):
    roteiro = get_object_or_404(Roteiro, pk=id) 
    roteiro.delete()
    messages.warning(request, "Usuário removido com sucesso!")
    return redirect("roteiros-view")

# Função para editar um roteiro
def editRoteiro(request, id):
    roteiro = get_object_or_404(Roteiro, pk=id)
    form = RoteiroForm(request.POST or None, instance=roteiro) #formulário preenchido com os dados do roteiro
    if form.is_valid(): 
        destino = form.cleaned_data["destino"]
        data_ida = form.cleaned_data["data_ida"]
        data_volta = form.cleaned_data["data_volta"]
        quantidade_pessoas = form.cleaned_data["quantidade_pessoas"]

        texto_usuario = f"Faça um roteiro de viagem para {destino}. Na data de {data_ida} à {data_volta}. Com {quantidade_pessoas} pessoas. Separe por tabela: Dia, turno, atividade e custo as sugestões."
        resposta_chatgpt = gerar_resposta(texto_usuario) 
        roteiro.resposta_chatgpt = resposta_chatgpt # Atualiza a resposta do chatgpt
        messages.warning(request, "Roteiro atualizado.")
        form.save()
        return render(
            request, "main/edit-roteiro.html", {"resposta": resposta_chatgpt}
        )  # Renderiza o template com a nova resposta do chatgpt

    return render(
        request,
        "main/edit-roteiro.html",
        {
            "form": form,
            "roteiro": roteiro,
            "resposta": roteiro.resposta_chatgpt,
        }, # Renderiza o template com o formulário preenchido e a resposta anterior do chatgpt
    )
 