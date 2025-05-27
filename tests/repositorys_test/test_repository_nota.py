from sys import path
from os import getenv
from datetime import date

from dotenv import load_dotenv
from pytest import mark


load_dotenv()

PROJECT_ROOT = getenv("PROJECT_ROOT")
path.insert(0, PROJECT_ROOT)

from app.repository.repository_nota import RepositoryNota
from app.model.model_nota import ModelNota


@mark.repository
class TestRepositoryNota:
    def test_criar_tabelas(self):
        try:
            repository_teste = RepositoryNota()
            repository_teste.database = getenv("DB_FILE_TEST")

            repository_teste.criar_tabelas()
            tabelas = ["clientes", "notas"]

            query = """
            SELECT name FROM sqlite_master
            WHERE type='table' AND name=?
            """

            for tabela in tabelas:
                repository_teste.conectar()
                existe = repository_teste.cursor.execute(query, (tabela,))
                if not existe:
                    raise ValueError(f"A tabela: {tabela} não foi criada ")
                repository_teste.desconectar()

            query = """
            SELECT name FROM sqlite_master
            WHERE type='view' AND name=?
            """
            view = "vw_relatorios"

            repository_teste.conectar()
            repository_teste.cursor.execute(query, (view,))
            repository_teste.desconectar()

            assert True

        except Exception as error:
            print("Tipo do erro:", type(error).__name__)
            print("Mensagem:", str(error))
            assert False

    def test_inserir_dados_na_tabela(self):
        try:
            repository_teste = RepositoryNota()
            repository_teste.database = getenv("DB_FILE_TEST")

            repository_teste.criar_tabelas()

            id_teste = 2
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

            repository_teste.inserir(nota_teste)

            query = """SELECT * FROM notas"""
            repository_teste.conectar()
            existe = repository_teste.cursor.execute(query).fetchone()

            if not existe:
                raise ValueError(f"Cliente não foi inserido")

            repository_teste.desconectar()

            assert True

        except Exception as error:
            print("Tipo do erro:", type(error).__name__)
            print("Mensagem:", str(error))
            assert False

    def test_retirar_dados_na_tabela(self):
        try:
            repository_teste = RepositoryNota()
            repository_teste.database = getenv("DB_FILE_TEST")

            dados = repository_teste.retirar(0)

            if len(dados) == 0:
                raise ValueError(f"Dados não estão sendo retornados")

            assert True

        except Exception as error:
            print("Tipo do erro:", type(error).__name__)
            print("Mensagem:", str(error))
            assert False

    def test_contar_paginas_na_tabela(self):
        try:
            repository_teste = RepositoryNota()
            repository_teste.database = getenv("DB_FILE_TEST")

            paginas = repository_teste.contar_pagina()

            if paginas == 1:
                assert True
            else:
                raise ValueError(f"Dados não estão sendo retornados direito")

        except Exception as error:
            print("Tipo do erro:", type(error).__name__)
            print("Mensagem:", str(error))
            assert False

    def test_modificar_dados_na_tabela(self):
        try:
            repository_teste = RepositoryNota()
            repository_teste.database = getenv("DB_FILE_TEST")

            repository_teste.criar_tabelas()

            id_teste = 2
            centro_de_custo_teste = "Teste_alterado"
            numero_nota_teste = "456"
            valor_nota_teste = 456.7
            data_fat_teste = date(2024, 7, 21).strftime("%d/%m/%Y")
            data_pag_teste = date(2024, 7, 21).strftime("%d/%m/%Y")
            mes_ref_teste = 7
            ano_ref_teste = 2024

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

            repository_teste.modificar(nota_teste_alterada)

            verificar = repository_teste.retirar(0)

            assert verificar[0].__dict__ == nota_teste_alterada.__dict__

        except Exception as error:
            print("Tipo do erro:", type(error).__name__)
            print("Mensagem:", str(error))
            assert False

    def test_deletar_dados_na_tabela(self):
        try:
            repository_teste = RepositoryNota()
            repository_teste.database = getenv("DB_FILE_TEST")

            repository_teste.criar_tabelas()

            id_teste = 2
            centro_de_custo_teste = "Teste_alterado"
            numero_nota_teste = "456"
            valor_nota_teste = 456.7
            data_fat_teste = date(2024, 7, 21).strftime("%d/%m/%Y")
            data_pag_teste = date(2024, 7, 21).strftime("%d/%m/%Y")
            mes_ref_teste = 7
            ano_ref_teste = 2024

            nota_teste_deletada = ModelNota(
                id_teste,
                centro_de_custo_teste,
                numero_nota_teste,
                valor_nota_teste,
                data_fat_teste,
                data_pag_teste,
                mes_ref_teste,
                ano_ref_teste,
            )

            repository_teste.deletar(nota_teste_deletada)

            verificar = repository_teste.retirar(0)

            assert len(verificar) == 0

        except Exception as error:
            print("Tipo do erro:", type(error).__name__)
            print("Mensagem:", str(error))
            assert False
