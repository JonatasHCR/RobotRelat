from sys import path
from os import getenv
from datetime import date
from sqlite3 import connect

from dotenv import load_dotenv
from pytest import mark

load_dotenv()

PROJECT_ROOT = getenv("PROJECT_ROOT")
path.insert(0, PROJECT_ROOT)

from app.service.service_nota import ServiceNota
from app.model.model_nota import ModelNota


@mark.service
class TestServiceCliente:
    def test_inserir_dados_formatados_na_tabela(self):
        try:
            service_teste = ServiceNota()

            id_teste = 3
            centro_de_custo_teste = "   Teste    "
            numero_nota_teste = "123   "
            valor_nota_teste = "123,4"
            data_fat_teste = date.today().strftime("%d/%m/%Y")
            data_pag_teste = date.today().strftime("%d/%m/%Y")
            mes_ref_teste = "2  "
            ano_ref_teste = "2025  "

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
            nota_teste_copy = nota_teste.__dict__.copy()
            
            service_teste.repository.database = getenv("DB_FILE_TEST")
            service_teste.inserir(nota_teste)

            connection = connect(getenv("DB_FILE_TEST"))
            curso = connection.cursor()

            verificar = curso.execute("SELECT * FROM notas").fetchone()

            assert not ModelNota(*verificar).__dict__ == nota_teste_copy
            assert ModelNota(*verificar).__dict__ == service_teste.formatar(ModelNota(**nota_teste_copy)).__dict__

        
        except Exception as error:
            print("Tipo do erro:", type(error).__name__)
            print("Mensagem:", str(error))
            assert False