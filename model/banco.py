'''
banco.py

modulo que estará contendo a classe que tem funções de manipulação 
de banco de dados(CRUD).

'''
#importação para criar caminho para o banco
import os

#importação para funcionamento da classe do banco
import sqlite3

ROOT_DIR = 'model'
DB_NAME = 'db.sqlite3'
DB_FILE = os.path.join(ROOT_DIR,DB_NAME)

#constante para o limite de registros
LIMIT_REGISTRO = 10

class DatabasePro:
    def __init__(self):
        self.criar_banco()
    
    def conectar(self)->None:
        self.connection = sqlite3.connect(DB_FILE)
        self.cursor = self.connection.cursor()
    
    def desconectar(self)->None:
        self.cursor.close()
        self.connection.close()
        

    def criar_banco(self)->None:
        try:
            self.conectar()

            # Ativar suporte a chaves estrangeiras
            self.cursor.execute("PRAGMA foreign_keys = ON;")

            # Criando tabela clientes 
            self.cursor.execute(
                f'CREATE TABLE IF NOT EXISTS clientes'
                '('
                'cliente TEXT,'
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

    def inserir_cliente(self,cliente:str,centro_de_custo:str,descricao:str,tipo:str)->None:
        try:
            self.conectar()

            #inserindo os valores
            self.cursor.execute('''
            INSERT INTO clientes (cliente,cc,descricao,tipo) VALUES (?,?,?,?)
        ''', (cliente,centro_de_custo,descricao,tipo,)
            )

            self.connection.commit()
        finally:
            self.desconectar()

    def inserir_nota(self,centro_de_custo:str,numero_nota:str,valor:float,data_fat:str,data_pag:str,mes_ref:str,ano_ref:str):
        try:
            self.conectar()

            #inserindo os valores
            self.cursor.execute('''
            INSERT INTO notas (cc,numero_nota,valor_nota,data_fat,data_pag,mes_ref,ano_ref) VALUES (?,?,?,?,?,?,?)
        ''', (centro_de_custo,numero_nota,valor,data_fat,data_pag,mes_ref,ano_ref,)
            )
            
            self.connection.commit()
        finally:
            self.desconectar()

    def verificar_centro_custo(self,centro_custo:str)->bool:
        try:
            self.conectar()
        
            self.cursor.execute('SELECT COUNT(*) FROM clientes WHERE cc = ?',(centro_custo,))

            existe = True if self.cursor.fetchone()[0] else False

            return existe

        finally:
            self.desconectar()
    def contar_pagina(self,all:bool=False,cliente:bool=False,notas:bool=False)->int:
        try:
            self.conectar()

            if all:
                self.cursor.execute('SELECT COUNT(*) FROM clientes JOIN notas ON clientes.cc = notas.cc')
            elif cliente:
                self.cursor.execute('SELECT COUNT(*) FROM clientes')
            elif notas:
                self.cursor.execute('SELECT COUNT(*) FROM notas')
            
            total_de_dados = self.cursor.fetchone()[0]
            
            total_de_paginas =  total_de_dados // LIMIT_REGISTRO

            if total_de_paginas < total_de_dados / LIMIT_REGISTRO:
                total_de_paginas += 1

            return total_de_paginas
        
        finally:
            self.desconectar

    def retirar_clientes(self,pagina_atual:int)->list[list]:
        try:
            self.conectar()
            
            self.cursor.execute('SELECT * FROM clientes LIMIT ? OFFSET ? ',(LIMIT_REGISTRO,pagina_atual*LIMIT_REGISTRO,))
            clientes = self.cursor.fetchall()
            
            
            return clientes
                    
        finally:
            self.desconectar()

    def retirar_notas(self,pagina_atual:int,remove_id:bool = True)->list[list]:
        try:
            self.conectar()
            
            if remove_id:
                self.cursor.execute(f"PRAGMA table_info(notas)")
                colunas_notas = [coluna[1] for coluna in self.cursor.fetchall()]
                colunas_notas.remove('id')
                
                self.cursor.execute('SELECT '+', '.join(colunas_notas)+' FROM notas LIMIT ? OFFSET ? ',(LIMIT_REGISTRO,pagina_atual*LIMIT_REGISTRO,))
            else:
                self.cursor.execute('SELECT * FROM notas LIMIT ? OFFSET ? ',(LIMIT_REGISTRO,pagina_atual*LIMIT_REGISTRO,))
            notas = self.cursor.fetchall()
            
            
            return notas
                    
        finally:
            self.desconectar


    def retirar_all(self,pagina_atual:int)->list[list]:
        try:
            self.conectar()
            
            self.cursor.execute(f"PRAGMA table_info(clientes)")
            colunas_clientes = ['clientes.'+coluna[1] for coluna in self.cursor.fetchall()]

            self.cursor.execute(f"PRAGMA table_info(notas)")
            colunas_notas = ['notas.'+coluna[1] for coluna in self.cursor.fetchall()]
            colunas_notas.remove('notas.id')
            colunas_notas.remove('notas.cc')
            colunas_notas.remove('notas.numero_nota')
            
            colunas_clientes.extend(colunas_notas)
            def organizar(list,list_ordem):
                lista_organizada = []
                for ordem in list_ordem:
                    lista_organizada.append(list[ordem])

                return lista_organizada
            
            colunas_clientes = organizar(colunas_clientes,[0,2,4,1,5,6,3])
            
            self.cursor.execute('SELECT '+', '.join(colunas_clientes)+' FROM clientes JOIN notas ON clientes.cc = notas.cc LIMIT ? OFFSET ? ',(LIMIT_REGISTRO,pagina_atual*LIMIT_REGISTRO,))
            clientes = self.cursor.fetchall()

            return clientes
                    
        finally:
            self.desconectar()

    def modificar_cliente(self,cliente:str,centro_de_custo:str,descricao:str,tipo:str,centro_de_custo_velho:str)->None:
        try:
            self.conectar()
            
            self.cursor.execute('''
            UPDATE clientes
            SET cliente = ?, cc = ?, descricao = ?, tipo = ?
            WHERE cc = ?;
        ''', (cliente,centro_de_custo,descricao,tipo,centro_de_custo_velho,)
            )
            self.connection.commit()
        finally:
            self.desconectar()

    def modificar_nota(self,id:int,centro_de_custo:str,numero_nota:str,valor:float,data_fat:str,data_pag:str,mes_ref:str,ano_ref:str)->None:
        
        try:
            self.conectar()
            self.cursor.execute('''
            UPDATE notas
            SET cc = ?, numero_nota = ?, valor_nota = ?, data_fat = ?, data_pag = ?,mes_ref = ?, ano_ref = ?
            WHERE id = ?
        ''', (centro_de_custo,numero_nota,valor,data_fat,data_pag,mes_ref,ano_ref,id,)
            )
            self.connection.commit()
        finally:
            self.desconectar()
if __name__ == '__main__':
    banco = DatabasePro()