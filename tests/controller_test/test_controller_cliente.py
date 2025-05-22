from sys import path
from os import getenv
from sqlite3 import connect

from dotenv import load_dotenv
from pytest import mark

load_dotenv()

PROJECT_ROOT = getenv("PROJECT_ROOT")
path.insert(0, PROJECT_ROOT)

from app.service.service_cliente import ServiceCliente
from app.model.model_cliente import ModelCliente


@mark.service
class TestControllerCliente:
    def test_inserir_dados_na_tabela(self):
        pass
