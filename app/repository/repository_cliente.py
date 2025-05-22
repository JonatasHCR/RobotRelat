"""
repository_cliente.py

modulo que estará contendo a classe que cria o banco de dados,
e faz manipulação da tabela clientes, cadastrar, alterar, deletar,
retirar.

"""

# importações para que consiga importar desde a raiz do projeto
import os
import sys
import sqlite3

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, PROJECT_ROOT)

import dotenv

from model.model_cliente import ModelCliente

dotenv.load_dotenv()

LIMIT_REGISTRO = int(os.getenv("LIMIT_REGISTRO"))


class RepositoryCliente:
    def __init__(self) -> None:
        self.database = os.getenv("DB_FILE")
        self.criar_tabelas()

    def conectar(self) -> None:
        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()

    def desconectar(self) -> None:
        self.cursor.close()
        self.connection.close()

    def criar_tabelas(self) -> None:
        try:
            self.conectar()

            # Ativar suporte a chaves estrangeiras
            self.cursor.execute("PRAGMA foreign_keys = ON;")

            # Criando tabela clientes
            query = """
            CREATE TABLE IF NOT EXISTS clientes(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT,
                cc TEXT UNIQUE,
                tipo TEXT,
                descricao TEXT
            )"""

            self.cursor.execute(query)

            # Criando tabela notas, com a chave
            # estrangeira da tabela clientes
            query = """
            CREATE TABLE IF NOT EXISTS notas(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cc TEXT NOT NULL,
                numero_nota TEXT,
                valor_nota INTEGER,
                data_fat TEXT,
                data_pag TEXT,
                mes_ref INTEGER,
                ano_ref INTEGER,
                FOREIGN KEY (cc) REFERENCES clientes (cc) ON DELETE CASCADE
            )"""

            self.cursor.execute(query)

            # Criando a view relatório
            query = """
            CREATE VIEW IF NOT EXISTS vw_relatorios AS
            SELECT
                clientes.nome AS nome,
                clientes.tipo AS tipo,
                notas.valor_nota AS valor,
                clientes.cc AS cc,
                notas.data_fat AS data_fat,
                notas.data_pag AS data_pag,
                clientes.descricao AS descricao,
                notas.mes_ref AS mes_ref,
                notas.ano_ref AS ano_ref
            FROM clientes
            JOIN notas ON notas.cc = clientes.cc;
            """

            self.cursor.execute(query)

            self.connection.commit()
        finally:
            self.desconectar()

    def inserir(self, cliente: ModelCliente) -> None:
        try:
            self.conectar()

            query = """
            INSERT INTO clientes
                (nome,cc,descricao,tipo)
            VALUES 
                (?,?,?,?)
            """
            # inserindo os valores
            self.cursor.execute(
                query,
                (
                    cliente.nome,
                    cliente.cc,
                    cliente.descricao,
                    cliente.tipo,
                ),
            )

            self.connection.commit()
        finally:
            self.desconectar()

    def verificar_centro_custo(self, centro_custo: str) -> bool:
        try:
            self.conectar()

            query = """
            SELECT 
                COUNT(*) 
            FROM clientes 
            WHERE 
                cc = ?"""

            self.cursor.execute(query, (centro_custo,))

            existe = True if self.cursor.fetchone()[0] else False

            return existe

        finally:
            self.desconectar()

    def contar_pagina(self) -> int:
        try:
            self.conectar()

            query = """
            SELECT 
                COUNT(*) 
            FROM clientes"""
            self.cursor.execute(query)

            total_de_dados = self.cursor.fetchone()[0]

            total_de_paginas = total_de_dados // LIMIT_REGISTRO

            if total_de_paginas < total_de_dados / LIMIT_REGISTRO:
                total_de_paginas += 1

            return total_de_paginas

        finally:
            self.desconectar()

    def retirar(self, pagina_atual: int) -> list[ModelCliente]:
        try:
            self.conectar()

            self.cursor.execute(
                "SELECT * FROM clientes LIMIT ? OFFSET ? ",
                (
                    LIMIT_REGISTRO,
                    pagina_atual * LIMIT_REGISTRO,
                ),
            )

            clientes = []

            dados = self.cursor.fetchall()
            if dados:
                for cliente in dados:
                    clientes.append(ModelCliente(*cliente))

            return clientes

        finally:
            self.desconectar()

    def modificar(self, cliente: ModelCliente) -> None:
        try:
            self.conectar()

            query = """
            UPDATE clientes
            SET nome = ?, cc = ?, descricao = ?, tipo = ?
            WHERE id = ?;"""

            self.cursor.execute(
                query,
                (
                    cliente.nome,
                    cliente.cc,
                    cliente.descricao,
                    cliente.tipo,
                    cliente.id,
                ),
            )

            self.connection.commit()
        finally:
            self.desconectar()

    def deletar(self, cliente: ModelCliente):
        try:
            self.conectar()

            self.cursor.execute("DELETE FROM clientes WHERE id = ?", (cliente.id,))

            self.connection.commit()
        finally:
            self.desconectar()

    def pesquisar(self):
        try:
            self.conectar()
        finally:
            self.desconectar()
