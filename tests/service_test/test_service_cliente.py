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
class TestServiceCliente:
    def test_inserir_dados_formatados_na_tabela(self):
        try:
            service_teste = ServiceCliente()

            id_teste = 3
            nome_teste = "    Teste      "
            centro_de_custo_teste = "   Teste    "
            tipo_teste = "    Próprio    "
            descricao_teste = "    teste testando      "

            cliente_teste = ModelCliente(
                id_teste, nome_teste, centro_de_custo_teste, tipo_teste, descricao_teste
            )
            cliente_teste_copy = cliente_teste.__dict__.copy()

            service_teste.repository.database = getenv("DB_FILE_TEST")
            service_teste.inserir(cliente_teste)

            connection = connect(getenv("DB_FILE_TEST"))
            curso = connection.cursor()

            verificar = curso.execute("SELECT * FROM clientes").fetchone()

            assert not ModelCliente(*verificar).__dict__ == cliente_teste_copy
            assert (
                ModelCliente(*verificar).__dict__
                == service_teste.formatar(ModelCliente(**cliente_teste_copy)).__dict__
            )

        except Exception as error:
            print("Tipo do erro:", type(error).__name__)
            print("Mensagem:", str(error))
            assert False

    def test_modificar_dados_formatados_na_tabela(self):
        try:
            service_teste = ServiceCliente()

            id_teste = 3
            nome_teste = "    Teste alterado      "
            centro_de_custo_teste = "   Teste alterado    "
            tipo_teste = "    Consorcio    "
            descricao_teste = "    teste testando alterado      "

            cliente_teste_alterado = ModelCliente(
                id_teste, nome_teste, centro_de_custo_teste, tipo_teste, descricao_teste
            )
            cliente_teste_alterado_copy = cliente_teste_alterado.__dict__.copy()

            service_teste.repository.database = getenv("DB_FILE_TEST")
            service_teste.modificar(cliente_teste_alterado)

            connection = connect(getenv("DB_FILE_TEST"))
            curso = connection.cursor()

            verificar = curso.execute("SELECT * FROM clientes").fetchone()

            assert (
                ModelCliente(*verificar).__dict__
                == service_teste.formatar(
                    ModelCliente(**cliente_teste_alterado_copy)
                ).__dict__
            )

        except Exception as error:
            print("Tipo do erro:", type(error).__name__)
            print("Mensagem:", str(error))
            assert False

    def test_retirar_dados_formatados_na_tabela(self):
        try:
            service_teste = ServiceCliente()

            id_teste = 3
            nome_teste = "    Teste alterado      "
            centro_de_custo_teste = "   Teste alterado    "
            tipo_teste = "    Consorcio    "
            descricao_teste = "    teste testando alterado      "

            cliente_teste_alterado = ModelCliente(
                id_teste, nome_teste, centro_de_custo_teste, tipo_teste, descricao_teste
            )

            service_teste.repository.database = getenv("DB_FILE_TEST")
            verificar = service_teste.retirar(0)

            assert (
                verificar[0].__dict__
                == service_teste.formatar(cliente_teste_alterado).__dict__
            )

        except Exception as error:
            print("Tipo do erro:", type(error).__name__)
            print("Mensagem:", str(error))
            assert False
    
    def test_contar_paginas_na_tabela(self):
        try:
            service_teste = ServiceCliente()

            service_teste.repository.database = getenv("DB_FILE_TEST")
            verificar = service_teste.paginas()

            assert verificar == 1

        except Exception as error:
            print("Tipo do erro:", type(error).__name__)
            print("Mensagem:", str(error))
            assert False

    def test_deletar_dados_formatados_na_tabela(self):
        try:
            service_teste = ServiceCliente()

            id_teste = 3
            nome_teste = "    Teste alterado      "
            centro_de_custo_teste = "   Teste alterado    "
            tipo_teste = "    Consorcio    "
            descricao_teste = "    teste testando alterado      "

            cliente_teste_alterado = ModelCliente(
                id_teste, nome_teste, centro_de_custo_teste, tipo_teste, descricao_teste
            )

            service_teste.repository.database = getenv("DB_FILE_TEST")
            service_teste.deletar(cliente_teste_alterado)

            connection = connect(getenv("DB_FILE_TEST"))
            curso = connection.cursor()

            verificar = curso.execute("SELECT * FROM clientes").fetchone()

            if verificar:
                assert False

            assert True

        except Exception as error:
            print("Tipo do erro:", type(error).__name__)
            print("Mensagem:", str(error))
            assert False
