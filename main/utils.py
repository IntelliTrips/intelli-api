import requests
import urllib3
import ssl


class CustomHttpAdapter (requests.adapters.HTTPAdapter):
    # "Transport adapter" that allows us to use custom ssl_context.

    def __init__(self, ssl_context=None, **kwargs):
        self.ssl_context = ssl_context
        super().__init__(**kwargs)

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = urllib3.poolmanager.PoolManager(
            num_pools=connections, maxsize=maxsize,
            block=block, ssl_context=self.ssl_context)


def get_legacy_session():
    ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    ctx.options |= 0x4  # OP_LEGACY_SERVER_CONNECT
    session = requests.session()
    session.mount('https://', CustomHttpAdapter(ctx))
    return session


def obter_cidades_principais():
    url = "https://servicodados.ibge.gov.br/api/v1/localidades/distritos"
    response = get_legacy_session().get(url)

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
