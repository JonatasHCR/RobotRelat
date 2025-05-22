import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0,PROJECT_ROOT)

from utils.utils import UtilsPro
from model.model_relatorio import ModelRelatorio
from calendar import monthrange

import sqlite3

LIMIT_REGISTRO = int(os.getenv("LIMIT_REGISTRO"))

class RelatorioView:
    def __init__(self):
        self.utils = UtilsPro()
        self.database = os.getenv('DB_FILE')
    
    def conectar(self) -> None:
        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()
    
    def desconectar(self) -> None:
        self.cursor.close()
        self.connection.close()

    def contar_pagina(self) -> int:
        try:
            self.conectar()
            
            query = '''
            SELECT 
                COUNT(*) 
            FROM clientes 
            JOIN notas ON clientes.cc = notas.cc'''

            self.cursor.execute(query)
            
            total_de_dados = self.cursor.fetchone()[0]
            
            total_de_paginas =  total_de_dados // LIMIT_REGISTRO

            if total_de_paginas < total_de_dados / LIMIT_REGISTRO:
                total_de_paginas += 1

            return total_de_paginas
        
        finally:
            self.desconectar()
    
    def retirar(self, pagina: int)-> list[ModelRelatorio]:
        try:
            self.conectar()
            query = '''
            SELECT * FROM vw_relatorios
            LIMIT ? OFFSET ?'''
            self.cursor.execute(query,(LIMIT_REGISTRO,pagina*LIMIT_REGISTRO,))
            relatorio = self.cursor.fetchall()

            lista = []
            if relatorio:
                for dados in relatorio:
                    lista.append(ModelRelatorio(*dados))
            
            return lista
        
        finally:
            self.desconectar()
    
    def retirar_mes_atual(self,mes_ref: int, ano_ref: int) -> list[ModelRelatorio]:
        try:
            self.conectar()
            query = '''
            SELECT
                clientes.nome,
                clientes.tipo,
                SUM(notas.valor_nota),
                clientes.cc,
                
                CASE notas.data_fat
                    WHEN  '' THEN  '-'
                    ELSE 'SIM'
                END as data_faturada,
                
                CASE notas.data_pag
                    WHEN  '' THEN '-'
                    ELSE 'SIM'
                END as data_paga,
                
                clientes.descricao,
                notas.mes_ref,
                notas.ano_ref
            FROM clientes 
            JOIN notas ON clientes.cc = notas.cc  
            WHERE 
                notas.mes_ref = ? 
                AND notas.ano_ref = ?
            GROUP BY clientes.cc, data_faturada, data_paga
                '''
            self.cursor.execute(query,(mes_ref,ano_ref,))
            
            relatorio = self.cursor.fetchall()

            lista = []
            for dados in relatorio:
                lista.append(ModelRelatorio(*dados))

            
            
            return lista
        
        finally:
            self.desconectar()
    
    def retirar_mes_anterior(self, mes_ref: int, ano_ref: int) -> list[ModelRelatorio]:
        try:
            if mes_ref + 1 < 10:
                mes = f'0{mes_ref+1}'
            else:
                mes = str(mes_ref + 1)

            self.conectar()
            query = '''
            SELECT
                clientes.nome,
                clientes.tipo,
                SUM(notas.valor_nota),
                clientes.cc,
                
                CASE notas.data_fat
                    WHEN  '' THEN  '-'
                    ELSE 'SIM'
                END as data_faturada,
                
                CASE notas.data_pag
                    WHEN  '' THEN '-'
                    ELSE 'SIM'
                END as data_paga,
                
                clientes.descricao,
                notas.mes_ref,
                notas.ano_ref
            FROM clientes 
            JOIN notas ON clientes.cc = notas.cc
            WHERE 
                (notas.mes_ref < ? OR notas.ano_ref != ?)
                AND (strftime('%m', notas.data_pag) = ? OR notas.data_pag = '')
                AND notas.data_fat != '' 
            GROUP BY clientes.cc, data_faturada, data_paga'''
            
            self.cursor.execute(query, (mes_ref, ano_ref, mes,))
            
            relatorio = self.cursor.fetchall()

            lista = []

            for dados in relatorio:
                lista.append(ModelRelatorio(*dados))
            
            return lista
        
        finally:
            self.desconectar()
    
    def retirar_total_periodo(self, mes_ref: int, ano_ref: int) -> dict[str,dict[str,int]]:
        try:
            mes = mes_ref + 1

            total_dias = monthrange(ano_ref,mes)[1]
            
            if mes_ref + 1 < 10:
                mes = f'0{mes_ref+1}'
            else:
                mes = str(mes_ref + 1)
            
            self.conectar()
            
            query = f'''
            SELECT
                clientes.tipo,
                CASE
                    WHEN strftime('%d', notas.data_pag) BETWEEN '01' AND '10' THEN 'PAGOS 1-10'
                    WHEN strftime('%d', notas.data_pag) BETWEEN '11' AND '20' THEN 'PAGOS 11-20'
                    WHEN strftime('%d', notas.data_pag) BETWEEN '21' AND '{total_dias}' THEN 'PAGOS 21-{total_dias}'
                END AS periodo,
                COALESCE(SUM(notas.valor_nota),0)
            FROM clientes 
            JOIN notas ON clientes.cc = notas.cc
            WHERE
                strftime('%Y-%m', notas.data_pag) = '{ano_ref}-{mes}'
            GROUP BY clientes.tipo,periodo; 
                '''
            
            self.cursor.execute(query)

            relatorio = self.cursor.fetchall()

            dicionario_periodo = dict([('PAGOS 1-10', 0), ('PAGOS 11-20',0), (f'PAGOS 21-{total_dias}',0)])
            dicionario = dict([("Próprio", dicionario_periodo.copy()),("Consórcio", dicionario_periodo.copy())])

            for tipo,periodo,valor in relatorio:
                dicionario[tipo][periodo] = valor

            return dicionario
        
        finally:
            self.desconectar()
