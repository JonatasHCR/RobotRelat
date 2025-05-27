from sys import path
from os import getenv
from datetime import date

from dotenv import load_dotenv
from pytest import mark

load_dotenv()

PROJECT_ROOT = getenv("PROJECT_ROOT")
path.insert(0, PROJECT_ROOT)

from app.repository.relatorio_view import RelatorioView
from app.repository.repository_cliente import RepositoryCliente
from app.repository.repository_nota import RepositoryNota
from app.model.model_cliente import ModelCliente
from app.model.model_nota import ModelNota


@mark.repository
class TestRelatorioView:
    def test_retirar_dados_na_tabela(self):
        try:
            repository_teste_cliente = RepositoryCliente()
            repository_teste_cliente.database = getenv("DB_FILE_TEST")
            repository_teste_cliente.criar_tabelas()

            id_teste = 1
            nome_teste = "Teste"
            centro_de_custo_teste = "Teste"
            tipo_teste = "Próprio"
            descricao_teste = "teste testando"

            cliente_teste = ModelCliente(
                id_teste, nome_teste, centro_de_custo_teste, tipo_teste, descricao_teste
            )

            repository_teste_cliente.inserir(cliente_teste)

            repository_teste_nota = RepositoryNota()
            repository_teste_nota.database = getenv("DB_FILE_TEST")
            repository_teste_nota.criar_tabelas()

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

            repository_teste_nota.inserir(nota_teste)

            repository_teste = RelatorioView()
            repository_teste.database = getenv("DB_FILE_TEST")

            dados = repository_teste.retirar(0)

            if len(dados) == 0:
                raise ValueError(f"Dados não estão sendo retornados")

            repository_teste_cliente.deletar(cliente_teste)
            repository_teste_nota.deletar(nota_teste)

            assert True

        except Exception as error:
            print("Tipo do erro:", type(error).__name__)
            print("Mensagem:", str(error))
            assert False
    
    def test_contar_paginas_na_tabela(self):
        try:
            repository_teste = RelatorioView()
            repository_teste.database = getenv("DB_FILE_TEST")

            paginas = repository_teste.contar_pagina()

            if paginas == 0:
                assert True
            else:
                raise ValueError(f"Dados não estão sendo retornados direito")

        except Exception as error:
            print("Tipo do erro:", type(error).__name__)
            print("Mensagem:", str(error))
            assert False
