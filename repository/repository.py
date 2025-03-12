import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0,PROJECT_ROOT)

from repository.repository_cliente import RepositoryCliente
from repository.repository_nota import RepositoryNota
from model.model_cliente import ModelCliente
from model.model_nota import ModelNota
from model.model import ModelPro

import sqlite3

LIMIT_REGISTRO = 10 

class RepositoryPro:
    def __init__(self):
        self.cliente = RepositoryCliente()
        self.nota = RepositoryNota()
    
    def conectar(self) -> None:
        self.connection = sqlite3.connect(os.getenv('DB_FILE'))
        self.cursor = self.connection.cursor()
    
    def desconectar(self) -> None:
        self.cursor.close()
        self.connection.close()

    def contar_pagina(self) -> int:
        try:
            self.conectar()

            self.cursor.execute('SELECT COUNT(*) FROM clientes JOIN notas ON clientes.cc = notas.cc')
            
            total_de_dados = self.cursor.fetchone()[0]
            
            total_de_paginas =  total_de_dados // LIMIT_REGISTRO

            if total_de_paginas < total_de_dados / LIMIT_REGISTRO:
                total_de_paginas += 1

            return total_de_paginas
        
        finally:
            self.desconectar()
    
    def retirar(self, pagina: int)-> list[ModelPro]:
        try:
            self.conectar()
            
            self.cursor.execute('SELECT clientes.nome,clientes.tipo,notas.valor_nota,clientes.cc,notas.data_fat,notas.data_pag,clientes.descricao,notas.mes_ref,notas.ano_ref FROM clientes JOIN notas ON clientes.cc = notas.cc LIMIT ? OFFSET ? ',(LIMIT_REGISTRO,pagina*LIMIT_REGISTRO,))
            relatorio = self.cursor.fetchall()

            lista = []

            for dados in relatorio:
                lista.append(ModelPro(*dados))
            
            return lista
        
        finally:
            self.desconectar()
    
    def retirar_mensal(self,mes_ref: int, ano_ref: int) -> list[ModelPro]:
        try:
            self.conectar()
            
            self.cursor.execute('SELECT clientes.nome,clientes.tipo,GROUP_CONCAT(notas.valor_nota,","),clientes.cc,GROUP_CONCAT(notas.data_fat, ","),GROUP_CONCAT(notas.data_pag, ","),clientes.descricao,notas.mes_ref,notas.ano_ref FROM clientes JOIN notas ON clientes.cc = notas.cc WHERE notas.mes_ref = ? AND notas.ano_ref = ? GROUP BY clientes.cc',(mes_ref,ano_ref,))
            
            relatorio = self.cursor.fetchall()

            lista = []

            for dados in relatorio:
                lista.append(ModelPro(*dados))
            
            return lista
        
        finally:
            self.desconectar()
    
    def retirar_all(self, mes_ref: int, ano_ref: int, data: str) -> list[ModelPro]:
        try:
            self.conectar()
            
            self.cursor.execute('''
            SELECT 
                clientes.nome,
                GROUP_CONCAT(clientes.tipo, ","),
                GROUP_CONCAT(notas.valor_nota, ","),
                clientes.cc,
                GROUP_CONCAT(notas.data_fat, ","),
                GROUP_CONCAT(notas.data_pag, ","),
                clientes.descricao,
                GROUP_CONCAT(notas.mes_ref, ","),
                GROUP_CONCAT(notas.ano_ref, ",")
            FROM clientes
            JOIN notas ON clientes.cc = notas.cc
            WHERE 
                (notas.mes_ref < ? OR notas.ano_ref != ?)
                AND (notas.data_pag <= ? OR notas.data_pag == '')
            GROUP BY clientes.cc
        ''', (mes_ref, ano_ref, data))
            
            relatorio = self.cursor.fetchall()

            lista = []

            for dados in relatorio:
                lista.append(ModelPro(*dados))
            
            return lista
        
        finally:
            self.desconectar()

if __name__ == "__main__":
    teste = RepositoryPro()
    teste.retirar(0)