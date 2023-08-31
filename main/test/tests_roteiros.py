from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User

roteiro_data = [{
        "partida": "Rio de Janeiro",
        "destino": "São Paulo",
        "data_ida": "2021-10-10",
        "data_volta": "2021-10-20",
        "quantidade_pessoas": 2,
        "custo": 1000.00,
    },
    {
        "partida": "Recife",
        "destino": "São Paulo",
        "data_ida": "2021-10-10",
        "data_volta": "2021-10-20",
        "quantidade_pessoas": 1,
        "custo": 2000.00,
    }
]

class RoteirosTestCase(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="123456"
        )
        print('Criou superuser')
        self.list_url = reverse("api:Roteiro-list") 
        self.client.login(username="admin", password="123456") 
        print('Fez login')
        print('Fazendo o roteiro...')
        self.client.post(self.list_url, data=roteiro_data[0])  
    
    def test_requisicao_1_get_para_listar_roteiros(self):
        """Teste para verificar se a requisição GET retorna o status code 200"""
        print('Listando roteiros...')
        response = self.client.get(self.list_url)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  
    
    def test_requisicao_2_put_para_alterar_roteiro(self):
        """Teste para verificar se a requisição PUT retorna o status code 200"""
        print('Alterando roteiro...')
        data = {
            "partida": "Salvador",
            "destino": "Rio de Janeiro",
            "data_ida": "2021-10-10",
            "data_volta": "2021-10-20",
            "quantidade_pessoas": 1,
            "custo": 2000.00,
        }
        response = self.client.put(reverse("api:Roteiro-detail", args=[1]), data=data)
        updated_data = self.client.get(self.list_url).data
        print(updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(updated_data[0]['partida'], "Salvador")
    
    def test_requisicao_3_delete_para_deletar_roteiro(self):
        """Teste para verificar se a requisição DELETE retorna o status code 204"""
        print('Deletando roteiro...')
        response = self.client.delete(reverse("api:Roteiro-detail", args=[1]))
        print(self.client.get(self.list_url))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_requisicao_4_nao_autorizada(self):
            """Teste para verificar se a requisição não autorizada retorna o status code 401"""
            self.client.logout()
            print('Fez logout')
            response = self.client.get(self.list_url)
            print('Tentado listar roteiros sem estar logado')
            print(response.data)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN) 

    
    
