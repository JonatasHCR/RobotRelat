from sys import path
from os import getenv

from dotenv import load_dotenv
from pytest import mark

load_dotenv()

PROJECT_ROOT = getenv("PROJECT_ROOT")
path.insert(0, PROJECT_ROOT)

from app.model.model_cliente import ModelCliente


@mark.models
class TestModelsCliente:
    def test_model_cliente(self):
        try:
            id_teste = 1
            nome_teste = "Teste"
            centro_de_custo_teste = "Teste"
            tipo_teste = "Próprio"
            descricao_teste = "teste testando"
            cliente_teste = ModelCliente(
                id_teste, nome_teste, centro_de_custo_teste, tipo_teste, descricao_teste
            )
            assert (
                cliente_teste.__str__()
                == f"{id_teste}|{nome_teste}|{centro_de_custo_teste}|{tipo_teste}|{descricao_teste}"
            )
        except Exception as error:
            print("Tipo do erro:", type(error).__name__)
            print("Mensagem:", str(error))
            assert False
