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
from app.service.service_cliente import ServiceCliente
from app.model.model_nota import ModelNota
from app.model.model_cliente import ModelCliente


@mark.service
class TestServiceNota:
    def test_inserir_dados_formatados_na_tabela(self):
        try:
            service_teste = ServiceCliente()

            id_teste = 4
            nome_teste = "    Teste      "
            centro_de_custo_teste = "   Teste    "
            tipo_teste = "    Próprio    "
            descricao_teste = "    teste testando      "

            cliente_teste = ModelCliente(
                id_teste, nome_teste, centro_de_custo_teste, tipo_teste, descricao_teste
            )

            service_teste.repository.database = getenv("DB_FILE_TEST")
            service_teste.inserir(cliente_teste)

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
            assert (
                ModelNota(*verificar).__dict__
                == service_teste.formatar(ModelNota(**nota_teste_copy)).__dict__
            )

        except Exception as error:
            print("Tipo do erro:", type(error).__name__)
            print("Mensagem:", str(error))
            assert False

    def test_modificar_dados_formatados_na_tabela(self):
        try:
            service_teste = ServiceCliente()

            id_teste = 4
            nome_teste = "    Teste      "
            centro_de_custo_teste = "   Teste alterado    "
            tipo_teste = "    Próprio    "
            descricao_teste = "    teste testando      "

            cliente_teste = ModelCliente(
                id_teste, nome_teste, centro_de_custo_teste, tipo_teste, descricao_teste
            )

            service_teste.repository.database = getenv("DB_FILE_TEST")
            service_teste.modificar(cliente_teste)

            service_teste = ServiceNota()

            id_teste = 3
            centro_de_custo_teste = "   Teste alterado    "
            numero_nota_teste = "456   "
            valor_nota_teste = "456,7"
            data_fat_teste = date(2026, 3, 12).strftime("%d/%m/%Y")
            data_pag_teste = date(2026, 3, 12).strftime("%d/%m/%Y")
            mes_ref_teste = "3  "
            ano_ref_teste = "2026  "

            nota_teste_alterada = ModelNota(
                id_teste,
                centro_de_custo_teste,
                numero_nota_teste,
                valor_nota_teste,
                data_fat_teste,
                data_pag_teste,
                mes_ref_teste,
                ano_ref_teste,
            )
            nota_teste_alterada_copy = nota_teste_alterada.__dict__.copy()

            service_teste.repository.database = getenv("DB_FILE_TEST")
            service_teste.modificar(nota_teste_alterada)

            connection = connect(getenv("DB_FILE_TEST"))
            curso = connection.cursor()

            verificar = curso.execute("SELECT * FROM notas").fetchone()

            assert (
                ModelNota(*verificar).__dict__
                == service_teste.formatar(
                    ModelNota(**nota_teste_alterada_copy)
                ).__dict__
            )

        except Exception as error:
            print("Tipo do erro:", type(error).__name__)
            print("Mensagem:", str(error))
            assert False

    def test_retirar_dados_formatados_na_tabela(self):
        try:
            service_teste = ServiceNota()

            id_teste = 3
            centro_de_custo_teste = "   Teste alterado    "
            numero_nota_teste = "456   "
            valor_nota_teste = "456,7"
            data_fat_teste = date(2026, 3, 12).strftime("%d/%m/%Y")
            data_pag_teste = date(2026, 3, 12).strftime("%d/%m/%Y")
            mes_ref_teste = "3  "
            ano_ref_teste = "2026  "

            nota_teste_alterada = ModelNota(
                id_teste,
                centro_de_custo_teste,
                numero_nota_teste,
                valor_nota_teste,
                data_fat_teste,
                data_pag_teste,
                mes_ref_teste,
                ano_ref_teste,
            )

            service_teste.repository.database = getenv("DB_FILE_TEST")
            verificar = service_teste.retirar(0)

            assert (
                verificar[0].__dict__
                == service_teste.utils.customizar(
                    [service_teste.formatar(nota_teste_alterada)]
                )[0].__dict__
            )

        except Exception as error:
            print("Tipo do erro:", type(error).__name__)
            print("Mensagem:", str(error))
            assert False

    def test_deletar_dados_formatados_na_tabela(self):
        try:
            service_teste = ServiceCliente()

            id_teste = 4
            nome_teste = "    Teste      "
            centro_de_custo_teste = "   Teste alterado    "
            tipo_teste = "    Próprio    "
            descricao_teste = "    teste testando      "

            cliente_teste = ModelCliente(
                id_teste, nome_teste, centro_de_custo_teste, tipo_teste, descricao_teste
            )

            service_teste.repository.database = getenv("DB_FILE_TEST")
            service_teste.deletar(cliente_teste)

            service_teste = ServiceNota()

            id_teste = 3
            centro_de_custo_teste = "   Teste alterado    "
            numero_nota_teste = "456   "
            valor_nota_teste = "456,7"
            data_fat_teste = date(2026, 3, 12).strftime("%d/%m/%Y")
            data_pag_teste = date(2026, 3, 12).strftime("%d/%m/%Y")
            mes_ref_teste = "3  "
            ano_ref_teste = "2026  "

            nota_teste_alterada = ModelNota(
                id_teste,
                centro_de_custo_teste,
                numero_nota_teste,
                valor_nota_teste,
                data_fat_teste,
                data_pag_teste,
                mes_ref_teste,
                ano_ref_teste,
            )

            service_teste.repository.database = getenv("DB_FILE_TEST")
            service_teste.deletar(nota_teste_alterada)

            connection = connect(getenv("DB_FILE_TEST"))
            curso = connection.cursor()

            verificar = curso.execute("SELECT * FROM notas").fetchone()

            if verificar:
                assert False

            assert True

        except Exception as error:
            print("Tipo do erro:", type(error).__name__)
            print("Mensagem:", str(error))
            assert False
