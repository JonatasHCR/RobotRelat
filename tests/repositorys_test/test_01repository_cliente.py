from sys import path
from os import getenv

from dotenv import load_dotenv
from pytest import mark

load_dotenv()

PROJECT_ROOT = getenv("PROJECT_ROOT")
path.insert(0, PROJECT_ROOT)

from app.repository.repository_cliente import RepositoryCliente
from app.model.model_cliente import ModelCliente


@mark.repository
class TestRepositoryCliente:
    def test_criar_tabelas(self):
        try:
            repository_teste = RepositoryCliente()
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
            repository_teste = RepositoryCliente()
            repository_teste.database = getenv("DB_FILE_TEST")

            repository_teste.criar_tabelas()
            
            id_teste = 1
            nome_teste = "Teste"
            centro_de_custo_teste = "Teste"
            tipo_teste = "Próprio"
            descricao_teste = "teste testando"
            
            cliente_teste = ModelCliente(
                id_teste, nome_teste, centro_de_custo_teste, tipo_teste, descricao_teste
            )
            
            repository_teste.inserir(cliente_teste)

            query = """SELECT * FROM clientes"""
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
            repository_teste = RepositoryCliente()
            repository_teste.database = getenv("DB_FILE_TEST")

            dados = repository_teste.retirar(0)

            if len(dados) == 0:
                raise ValueError(f"Dados não estão sendo retornados")

            assert True

        except Exception as error:
            print("Tipo do erro:", type(error).__name__)
            print("Mensagem:", str(error))
            assert False