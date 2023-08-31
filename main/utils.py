import requests


def obter_cidades_principais():
    url = "https://servicodados.ibge.gov.br/api/v1/localidades/distritos"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        cidades_principais = [
            distrito for distrito in data if distrito.get("municipio")
        ]

        CIDADES = []

        for cidade in cidades_principais:
            nome_cidade = cidade["municipio"]["nome"]
            uf = cidade["municipio"]["microrregiao"]["mesorregiao"]["UF"]["sigla"]
            CIDADES.append((f"{uf} - {nome_cidade}", f"{uf} - {nome_cidade}"))

        return sorted(CIDADES)
    else:
        return None


CIDADES = obter_cidades_principais()
