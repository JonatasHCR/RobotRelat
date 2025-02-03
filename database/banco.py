'''
banco.py

modulo que cria o banco de dados, e faz sua manipulação
'''

import sqlite3
import os

ROOT_DIR = 'database'
DB_NAME = 'db.sqlite3'
DB_FILE = os.path.join(ROOT_DIR,DB_NAME)

def criar_banco():
    try:
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()

        # Ativar suporte a chaves estrangeiras
        cursor.execute("PRAGMA foreign_keys = ON;")

        # Criando tabela clientes 
        cursor.execute(
            f'CREATE TABLE IF NOT EXISTS clientes'
            '('
            'cliente TEXT,'
            'centro_custo TEXT UNIQUE,'
            'descricao TEXT'
            ')'
        )
        
        # Criando tabela relatório, com a chave 
        # estrangeira da tabela clientes
        cursor.execute(
            f'CREATE TABLE IF NOT EXISTS notas'
            '('
            'cc TEXT NOT NULL,'
            'numero_nota TEXT,'
            'valor_nota REAL,'
            'data_fat TEXT,'
            'data_pag TEXT,'
            'FOREIGN KEY (cc) REFERENCES clientes (centro_custo) ON DELETE CASCADE'
            ')'
        )

        connection.commit()
    finally:
        cursor.close()
        connection.close()

def inserir_cliente(cliente,centro_de_custo,descricao):
    try:
        #Garantindo a criação do banco
        criar_banco()
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor() 

        #inserindo os valores
        cursor.execute('''
        INSERT INTO clientes (cliente,centro_custo,descricao) VALUES (?,?,?)
    ''', (cliente,centro_de_custo,descricao,)
        )

        connection.commit()
    finally:
        cursor.close()
        connection.close()

def inserir_nota(centro_de_custo,numero_nota,valor,data_fat,data_pag):
    try:
        #Garantindo a criação do banco
        criar_banco()
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor() 

        #inserindo os valores
        cursor.execute('''
        INSERT INTO notas (cc,numero_nota,valor_nota,data_fat,data_pag) VALUES (?,?,?,?,?)
    ''', (centro_de_custo,numero_nota,valor,data_fat,data_pag,)
        )
        
        connection.commit()
    finally:
        cursor.close()
        connection.close()
