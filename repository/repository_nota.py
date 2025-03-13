'''
repository_nota.py

modulo que estará contendo a classe que cria o banco de dados, 
e faz manipulação da tabela notas, cadastrar, alterar, deletar,
retirar.

'''

#importações para que consiga importar desde a raiz do projeto
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0,PROJECT_ROOT)

import sqlite3
import dotenv

dotenv.load_dotenv()

from model.model_nota import ModelNota

LIMIT_REGISTRO = 10 #os.getenv("LIMIT_REGISTRO")

class RepositoryNota:
    def __init__(self) -> None:
        self.criar_banco()
    
    def conectar(self) -> None:
        self.connection = sqlite3.connect(os.getenv('DB_FILE'))
        self.cursor = self.connection.cursor()
    
    def desconectar(self) -> None:
        self.cursor.close()
        self.connection.close()
        

    def criar_banco(self) -> None:
        try:
            self.conectar()

            # Ativar suporte a chaves estrangeiras
            self.cursor.execute("PRAGMA foreign_keys = ON;")

            # Criando tabela clientes 
            self.cursor.execute(
                f'CREATE TABLE IF NOT EXISTS clientes'
                '('
                'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                'nome TEXT,'
                'cc TEXT UNIQUE,'
                'tipo TEXT,'
                'descricao TEXT'
                ')'
            )
            
            # Criando tabela relatório, com a chave 
            # estrangeira da tabela clientes
            self.cursor.execute(
                f'CREATE TABLE IF NOT EXISTS notas'
                '('
                'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                'cc TEXT NOT NULL,'
                'numero_nota TEXT,'
                'valor_nota INTEGER,'
                'data_fat TEXT,'
                'data_pag TEXT,'
                'mes_ref INTEGER,'
                'ano_ref INTEGER,'
                'FOREIGN KEY (cc) REFERENCES clientes (cc) ON DELETE CASCADE'
                ')'
            )

            self.connection.commit()
        finally:
            self.desconectar()


    def inserir(self,nota: ModelNota) -> None:
        try:
            self.conectar()

            #inserindo os valores
            self.cursor.execute('''
            INSERT INTO notas (cc,numero_nota,valor_nota,data_fat,data_pag,mes_ref,ano_ref) VALUES (?,?,?,?,?,?,?)
        ''', (nota.cc,nota.numero_nota,nota.valor_nota,nota.data_fat,nota.data_pag,nota.mes_ref,nota.ano_ref,)
            )
            
            self.connection.commit()
        finally:
            self.desconectar()

    def verificar_centro_custo(self,centro_custo: str) -> bool:
        try:
            self.conectar()
        
            self.cursor.execute('SELECT COUNT(*) FROM clientes WHERE cc = ?',(centro_custo,))

            existe = True if self.cursor.fetchone()[0] else False

            return existe

        finally:
            self.desconectar()

    def contar_pagina(self) -> int:
        try:
            self.conectar()

            self.cursor.execute('SELECT COUNT(*) FROM notas')
            
            total_de_dados = self.cursor.fetchone()[0]
            
            total_de_paginas =  total_de_dados // LIMIT_REGISTRO

            if total_de_paginas < total_de_dados / LIMIT_REGISTRO:
                total_de_paginas += 1

            return total_de_paginas
        
        finally:
            self.desconectar()


    def retirar(self,pagina_atual: int) -> list[ModelNota]:
        try:
            self.conectar()
            
            self.cursor.execute('SELECT * FROM notas LIMIT ? OFFSET ? ',(LIMIT_REGISTRO,pagina_atual*LIMIT_REGISTRO,))
            
            notas = []
            for nota in self.cursor.fetchall():
                notas.append(ModelNota(*nota))
            
            return notas
                    
        finally:
            self.desconectar()

    def modificar(self,nota: ModelNota) -> None:
        
        try:
            self.conectar()
            
            self.cursor.execute('''
            UPDATE notas
            SET cc = ?, numero_nota = ?, valor_nota = ?, data_fat = ?, data_pag = ?,mes_ref = ?, ano_ref = ?
            WHERE id = ?
        ''', (nota.cc,nota.numero_nota,nota.valor_nota,nota.data_fat,nota.data_pag,nota.mes_ref,nota.ano_ref,nota.id,)
            )

            self.connection.commit()
        finally:
            self.desconectar()

    def deletar(self,nota: ModelNota) -> None:
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