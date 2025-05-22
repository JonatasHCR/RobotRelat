from sys import path
from os import getenv
from sqlite3 import connect

from dotenv import load_dotenv
from pytest import mark

load_dotenv()

PROJECT_ROOT = getenv("PROJECT_ROOT")
path.insert(0, PROJECT_ROOT)

from app.service.service_nota import ServiceNota
from app.model.model_nota import ModelNota


@mark.service
class TestControllerNota:
    def test_inserir_dados_na_tabela(self):
        pass
