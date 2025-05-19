from sys import path
from os import getenv
from datetime import date

from dotenv import load_dotenv
from pytest import mark

load_dotenv()

PROJECT_ROOT = getenv("PROJECT_ROOT")
path.insert(0, PROJECT_ROOT)

from app.model.model_relatorio import ModelRelatorio


@mark.models
class TestModelsNota:
    def test_model_cliente(self):
        try:
            nome_teste = "Teste"
            tipo_teste = "Próprio"
            centro_de_custo_teste = "Teste"
            valor_nota_teste = 123.4
            data_fat_teste = date.today().strftime("%d/%m/%Y")
            data_pag_teste = date.today().strftime("%d/%m/%Y")
            descricao_teste = "teste testando"
            mes_ref_teste = 2
            ano_ref_teste = 2025
            relatorio_teste = ModelRelatorio(
                nome_teste,
                tipo_teste,
                valor_nota_teste,
                centro_de_custo_teste,
                data_fat_teste,
                data_pag_teste,
                descricao_teste,
                mes_ref_teste,
                ano_ref_teste,
            )
            assert (
                relatorio_teste.__str__()
                == f"{nome_teste}|{tipo_teste}|{valor_nota_teste}|{centro_de_custo_teste}|{data_fat_teste}|{data_pag_teste}|{descricao_teste}"
            )
        except Exception as error:
            print("Tipo do erro:", type(error).__name__)
            print("Mensagem:", str(error))
            assert False
