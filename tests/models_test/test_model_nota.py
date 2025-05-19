from sys import path
from os import getenv
from datetime import date

from dotenv import load_dotenv
from pytest import mark

load_dotenv()

PROJECT_ROOT = getenv("PROJECT_ROOT")
path.insert(0, PROJECT_ROOT)

from app.model.model_nota import ModelNota


@mark.models
class TestModelsNota:
    def test_model_cliente(self):
        try:
            id_teste = 1
            centro_de_custo_teste = "Teste"
            numero_nota_teste = "123"
            valor_nota_teste = 123.4
            data_fat_teste = date.today().strftime("%d/%m/%Y")
            data_pag_teste = date.today().strftime("%d/%m/%Y")
            mes_ref_teste = 2
            ano_ref_teste = 2025
            nota_teste = ModelNota(
                id_teste,
                centro_de_custo_teste,
                numero_nota_teste,
                valor_nota_teste,
                data_fat_teste,
                data_pag_teste,
                mes_ref_teste,
                ano_ref_teste,
            )
            assert (
                nota_teste.__str__()
                == f"{id_teste}|{centro_de_custo_teste}|{numero_nota_teste}|{valor_nota_teste}|{data_fat_teste}|{data_pag_teste}|{mes_ref_teste}|{ano_ref_teste}"
            )
        except Exception as error:
            print("Tipo do erro:", type(error).__name__)
            print("Mensagem:", str(error))
            assert False
