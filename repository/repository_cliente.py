import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0,PROJECT_ROOT)

import sqlite3
import dotenv

from model.cliente import Cliente

dotenv.load_dotenv()

LIMIT_REGISTRO = 10 

class RepositoryCliente:
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
                'mes_ref TEXT,'
                'ano_ref TEXT,'
                'FOREIGN KEY (cc) REFERENCES clientes (cc) ON DELETE CASCADE'
                ')'
            )
            
            self.connection.commit()
        finally:
            self.desconectar()

    def inserir(self,cliente: Cliente) -> None:
        try:
            self.conectar()

            #inserindo os valores
            self.cursor.execute('''
            INSERT INTO clientes (nome,cc,descricao,tipo) VALUES (?,?,?,?)
        ''', (cliente.nome,cliente.cc,cliente.descricao,cliente.tipo,)
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

            self.cursor.execute('SELECT COUNT(*) FROM clientes')
            
            total_de_dados = self.cursor.fetchone()[0]
            
            total_de_paginas =  total_de_dados // LIMIT_REGISTRO

            if total_de_paginas < total_de_dados / LIMIT_REGISTRO:
                total_de_paginas += 1

            return total_de_paginas
        
        finally:
            self.desconectar()

    def retirar(self,pagina_atual: int) -> list[Cliente]:
        try:
            self.conectar()
            
            self.cursor.execute('SELECT * FROM clientes LIMIT ? OFFSET ? ',(LIMIT_REGISTRO,pagina_atual*LIMIT_REGISTRO,))

            clientes = []
            
            for cliente in self.cursor.fetchall():
                clientes.append(Cliente(*cliente))
            
            return clientes
                    
        finally:
            self.desconectar()


    def modificar(self,cliente: Cliente) -> None:
        try:
            self.conectar()
            
            self.cursor.execute('''
            UPDATE clientes
            SET nome = ?, cc = ?, descricao = ?, tipo = ?
            WHERE id = ?;
        ''', (cliente.nome,cliente.cc,cliente.descricao,cliente.tipo,cliente.id,)
            )

            self.connection.commit()
        finally:
            self.desconectar()

    def deletar(self,cliente: Cliente):
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