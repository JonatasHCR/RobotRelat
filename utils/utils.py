import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0,PROJECT_ROOT)

from sqlite3 import IntegrityError
import database.banco as banco

from datetime import datetime

def cadastrar_nota(texto_feedback, dicionario):
        centro_custo = dicionario['Centro de Custo'].get()
        dicionario['Centro de Custo'].delete(0,'end')

        numero_nota = dicionario['Numero da Nota'].get()
        dicionario['Numero da Nota'].delete(0,'end')

        valor_nota = dicionario['Valor da Nota'].get()
        dicionario['Valor da Nota'].delete(0,'end')

        data_fat = dicionario['Data de Faturamento'].get()
        dicionario['Data de Faturamento'].delete(0,'end')

        data_pag = dicionario['Data de Pagamento'].get()
        dicionario['Data de Pagamento'].delete(0,'end')

        centro_custo = centro_custo.strip()
        numero_nota = numero_nota.strip()
        valor_nota = float(valor_nota.strip().replace('.','').replace(',','.'))

        if data_pag != '':
            data_pag = data_pag.split('/')
            data_pag = datetime(day=int(data_pag[0]),month=int(data_pag[1]), year=int(data_pag[2])).strftime("%Y-%m-%d")
        
        if data_fat != '':
            data_fat = data_fat.split('/')
            data_fat = datetime(day=int(data_fat[0]),month=int(data_fat[1]), year=int(data_fat[2])).strftime("%Y-%m-%d")
        
        try:
            banco.inserir_nota(centro_custo,numero_nota,valor_nota,data_fat,data_pag)
            texto_feedback.configure(text='Nota cadastrada com sucesso!!', text_color='green')
        except IntegrityError:
            texto_feedback.configure(text='Erro ao cadastrar nota', text_color='red')

def cadastrar_cliente(texto_feedback, dicionario):
    
        cliente = dicionario['Cliente'].get()
        dicionario['Cliente'].delete(0,'end')
        
        centro_custo = dicionario['Centro de Custo'].get()
        dicionario['Centro de Custo'].delete(0,'end')
        
        descricao = dicionario['Descrição'].get()
        dicionario['Descrição'].delete(0,'end')

        cliente = cliente.strip()
        centro_custo = centro_custo.strip()
        descricao = descricao.strip()
        try:
            banco.inserir_cliente(cliente,centro_custo,descricao)
            texto_feedback.configure(text='Cliente cadastrado com sucesso!!', text_color='green')
        except IntegrityError:
            texto_feedback.configure(text='Centro de custo já cadastrado', text_color='red')

if __name__ == '__main__':
    pass
