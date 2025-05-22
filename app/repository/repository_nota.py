"""
repository_nota.py

modulo que estará contendo a classe que cria o banco de dados,
e faz manipulação da tabela notas, cadastrar, alterar, deletar,
retirar.

"""

# importações para que consiga importar desde a raiz do projeto
from os import getenv
from sys import path
from sqlite3 import connect

from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = getenv("PROJECT_ROOT")
path.insert(0, PROJECT_ROOT)

from app.model.model_nota import ModelNota

LIMIT_REGISTRO = int(getenv("LIMIT_REGISTRO"))


class RepositoryNota:
    def __init__(self) -> None:
        self.database = getenv("DB_FILE")
        self.criar_tabelas()

    def conectar(self) -> None:
        self.connection = connect(self.database)
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

    def inserir(self, nota: ModelNota) -> None:
        try:
            self.conectar()

            # inserindo os valores
            query = """
            INSERT INTO notas (
                cc,
                numero_nota,
                valor_nota,
                data_fat,
                data_pag,
                mes_ref,
                ano_ref
            ) VALUES (?,?,?,?,?,?,?)"""
            self.cursor.execute(
                query,
                (
                    nota.cc,
                    nota.numero_nota,
                    nota.valor_nota,
                    nota.data_fat,
                    nota.data_pag,
                    nota.mes_ref,
                    nota.ano_ref,
                ),
            )

            self.connection.commit()
        finally:
            self.desconectar()

    def verificar_centro_custo(self, centro_custo: str) -> bool:
        try:
            self.conectar()

            self.cursor.execute(
                "SELECT COUNT(*) FROM clientes WHERE cc = ?", (centro_custo,)
            )

            existe = True if self.cursor.fetchone()[0] else False

            return existe

        finally:
            self.desconectar()

    def contar_pagina(self) -> int:
        try:
            self.conectar()

            self.cursor.execute("SELECT COUNT(*) FROM notas")

            total_de_dados = self.cursor.fetchone()[0]

            total_de_paginas = total_de_dados // LIMIT_REGISTRO

            if total_de_paginas < total_de_dados / LIMIT_REGISTRO:
                total_de_paginas += 1

            return total_de_paginas

        finally:
            self.desconectar()

    def retirar(self, pagina_atual: int) -> list[ModelNota]:
        try:
            self.conectar()

            self.cursor.execute(
                "SELECT * FROM notas LIMIT ? OFFSET ? ",
                (
                    LIMIT_REGISTRO,
                    pagina_atual * LIMIT_REGISTRO,
                ),
            )

            notas = []

            dados = self.cursor.fetchall()
            if dados:
                for nota in dados:
                    notas.append(ModelNota(*nota))

            return notas

        finally:
            self.desconectar()

    def modificar(self, nota: ModelNota) -> None:

        try:
            self.conectar()

            query = """
            UPDATE notas
            SET 
                cc = ?, 
                numero_nota = ?, 
                valor_nota = ?, 
                data_fat = ?, 
                data_pag = ?,
                mes_ref = ?, 
                ano_ref = ?
            WHERE id = ?;"""

            self.cursor.execute(
                query,
                (
                    nota.cc,
                    nota.numero_nota,
                    nota.valor_nota,
                    nota.data_fat,
                    nota.data_pag,
                    nota.mes_ref,
                    nota.ano_ref,
                    nota.id,
                ),
            )

            self.connection.commit()
        finally:
            self.desconectar()

    def deletar(self, nota: ModelNota) -> None:
        try:
            self.conectar()

            self.cursor.execute("DELETE FROM notas WHERE id = ?", (nota.id,))

            self.connection.commit()
        finally:
            self.desconectar()

    def pesquisar(self):
        try:
            self.conectar()
        finally:
            self.desconectar()
