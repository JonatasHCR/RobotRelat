'''
banco.py

modulo que cria o banco de dados, e faz sua manipulação
'''

import os
import sqlite3

ROOT_DIR = 'database'
DB_NAME = 'db.sqlite3'
DB_FILE = os.path.join(ROOT_DIR,DB_NAME)

LIMIT_REGISTRO = 10

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
            'cc TEXT UNIQUE,'
            'descricao TEXT'
            ')'
        )
        
        # Criando tabela relatório, com a chave 
        # estrangeira da tabela clientes
        cursor.execute(
            f'CREATE TABLE IF NOT EXISTS notas'
            '('
            'id INTEGER PRIMARY KEY AUTOINCREMENT,'
            'cc TEXT NOT NULL,'
            'numero_nota TEXT,'
            'valor_nota INTEGER,'
            'data_fat TEXT,'
            'data_pag TEXT,'
            'FOREIGN KEY (cc) REFERENCES clientes (cc) ON DELETE CASCADE'
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
        INSERT INTO clientes (cliente,cc,descricao) VALUES (?,?,?)
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

def verificar_centro_custo(centro_custo):
    try:
        #Garantindo a criação do banco
        criar_banco()
        
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
       
        cursor.execute('SELECT COUNT(*) FROM clientes WHERE cc = ?',(centro_custo,))

        existe = True if cursor.fetchone()[0] else False

        return existe

    finally:
        cursor.close()
        connection.close()

def contar_pagina(all=False,cliente=False,notas=False):
    try:
        #Garantindo a criação do banco
        criar_banco()
        
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        if all:
            cursor.execute('SELECT COUNT(*) FROM clientes JOIN notas ON clientes.cc = notas.cc')
        elif cliente:
            cursor.execute('SELECT COUNT(*) FROM clientes')
        elif notas:
            cursor.execute('SELECT COUNT(*) FROM notas')
        
        total_de_dados = cursor.fetchone()[0]
        
        total_de_paginas =  total_de_dados // LIMIT_REGISTRO

        if total_de_paginas < total_de_dados / LIMIT_REGISTRO:
            total_de_paginas += 1

        return total_de_paginas
    
    finally:
        cursor.close()
        connection.close()

def retirar_clientes(pagina_atual):
    try:
        #Garantindo a criação do banco
        criar_banco()
        
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        
        
        cursor.execute('SELECT * FROM clientes LIMIT ? OFFSET ? ',(LIMIT_REGISTRO,pagina_atual*LIMIT_REGISTRO,))
        clientes = cursor.fetchall()
        
        
        return clientes
                
    finally:
        cursor.close()
        connection.close()

def retirar_notas(pagina_atual,remove_id = True):
    try:
        #Garantindo a criação do banco
        criar_banco()
        
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        
        if remove_id:
            cursor.execute(f"PRAGMA table_info(notas)")
            colunas_notas = [coluna[1] for coluna in cursor.fetchall()]
            colunas_notas.remove('id')
            
            cursor.execute('SELECT '+', '.join(colunas_notas)+' FROM notas LIMIT ? OFFSET ? ',(LIMIT_REGISTRO,pagina_atual*LIMIT_REGISTRO,))
        else:
            cursor.execute('SELECT * FROM clientes LIMIT ? OFFSET ? ',(LIMIT_REGISTRO,pagina_atual*LIMIT_REGISTRO,))
        notas = cursor.fetchall()
        
        
        return notas
                
    finally:
        cursor.close()
        connection.close()


def retirar_all(pagina_atual):
    try:
        #Garantindo a criação do banco
        criar_banco()
        
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        
        cursor.execute(f"PRAGMA table_info(clientes)")
        colunas_clientes = ['clientes.'+coluna[1] for coluna in cursor.fetchall()]

        cursor.execute(f"PRAGMA table_info(notas)")
        colunas_notas = ['notas.'+coluna[1] for coluna in cursor.fetchall()]
        colunas_notas.remove('notas.id')
        colunas_notas.remove('notas.cc')
        colunas_notas.remove('notas.numero_nota')
        
        colunas_clientes.extend(colunas_notas)
        def organizar(list,list_ordem):
            lista_organizada = []
            for ordem in list_ordem:
                lista_organizada.append(list[ordem])

            return lista_organizada
        
        colunas_clientes = organizar(colunas_clientes,[0,3,1,4,5,2])
        
        cursor.execute('SELECT '+', '.join(colunas_clientes)+' FROM clientes JOIN notas ON clientes.cc = notas.cc LIMIT ? OFFSET ? ',(LIMIT_REGISTRO,pagina_atual*LIMIT_REGISTRO,))
        clientes = cursor.fetchall()
        
        return clientes
                
    finally:
        cursor.close()
        connection.close()

def modificar_cliente(cliente,centro_de_custo,descricao):
    try:
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute('''
        UPDATE clientes
        SET cliente = ?, cc = ?, descricao = ?
        WHERE cc = ?;
    ''', (cliente,centro_de_custo,descricao,centro_de_custo,)
        )
        connection.commit()
    finally:
        cursor.close()
        connection.close()

def modificar_nota(id,centro_de_custo,numero_nota,valor,data_fat,data_pag):
    try:
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute('''
        UPDATE notas
        SET cc = ?, numero_nota = ?, valor_nota = ?, data_fat = ?, data_pag = ?
        WHERE id = ?;
    ''', (centro_de_custo,numero_nota,valor,data_fat,data_pag,id,)
        )
        connection.commit()
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    print(retirar_notas(1))