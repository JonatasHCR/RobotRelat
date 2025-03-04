'''
controller.py

modulo que estará contendo a classe que faz a ponte entre a parte
gráfica, e o banco de dados.

'''

#importações para que consiga importar 
#desde a raiz do projeto
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0,PROJECT_ROOT)

#importando o erro
from sqlite3 import IntegrityError

#importações para funcionamento da classe
from model.nota import Nota
from service.service_nota import ServiceNota
from utils.utils import UtilsPro

#importação para a tipagem
from customtkinter import CTkLabel

class ControllerNota:
    """
    Classe responsável pelo controle das operações do sistema financeiro.

    Atua como intermediária entre a interface gráfica e o banco de dados,
    realizando operações como cadastro, modificação e recuperação de notas e notas fiscais.
    """

    def __init__(self):
        """
        Inicializa a classe ControllerPro.
        
        Cria instâncias das classes DatabasePro e UtilsPro.
        """
        self.service = ServiceNota()
        self.utils = UtilsPro()

    def cadastrar(self, texto_feedback: CTkLabel, dicionario: dict) -> None:
        """
        Cadastra uma nota fiscal no banco de dados.

        param:
            texto_feedback(CTkLabel): Label para exibir mensagens de feedback ao usuário.
            dicionario(dict): Dicionário contendo os dados da nota a serem cadastrados.
        """

        quant = int(dicionario["Quantidade de Registros"].get())

        #pegando os dados
        centro_custo = dicionario['Centro de Custo'].get()
        numero_nota = dicionario['Numero da Nota'].get()
        valor_nota = dicionario['Valor da Nota'].get()
        data_fat = dicionario['Data de Faturamento'].get()
        data_pag = dicionario['Data de Pagamento'].get()
        mes_ref = dicionario["Mês de Referência"].get()
        ano_ref = dicionario['Ano de Referência'].get()

        nota = Nota('',centro_custo,numero_nota,valor_nota,data_fat,data_pag,mes_ref,ano_ref)

        try:   
            self.service.inserir(nota)
            texto_feedback.configure(text='Nota cadastrada com sucesso!!', text_color='green')
            self.utils.apagar_valores(dicionario,quant,nota=True)
        except:
            texto_feedback.configure(text='Erro ao cadastrar nota', text_color='red')

    def contar_pagina(self) -> int:
        """
        Conta o número de páginas disponíveis para notas.

        return: 
            (int): Número total de páginas.
        """
        return self.service.paginas()

    def retirar(self, pagina: int) -> list[Nota]:
        """
        Recupera a lista de notas fiscais cadastradas.

        param: 
            pagina(int): Número da página de registros a ser recuperada.
        return: 
            (list[list]): Lista contendo a lista de dados das notas fiscais.
        """
        return self.service.retirar(pagina)


    def modificar(self, dados: list[dict], texto_feedback: CTkLabel) -> None:
        """
        Modifica os dados de notas fiscais cadastradas.

        param:
            dados(list[dict]): Lista de dicionários contendo os novos dados das notas.
            texto_feedback(CTkLabel): Label para exibir mensagens de feedback ao usuário.
        """
        dado_error = []
        for dado in dados:

            #pegando os dados
            id_nota =  int(dado['id'].get())
            centro_custo = dado["Centro de Custo"].get()
            numero_nota = dado["Numero da Nota"].get()
            valor_nota = dado["Valor da Nota"].get()
            data_fat = dado["Data de Faturamento"].get()
            data_pag = dado["Data de Pagamento"].get()
            mes_ref = dado["Mês de Referência"].get()
            ano_ref = dado["Ano de Referência"].get()

            nota = Nota(id_nota,centro_custo,numero_nota,valor_nota,data_fat,data_pag,mes_ref,ano_ref)
            
            try:
                self.service.modificar(nota)
            except (IntegrityError,ValueError):
                dado_error.append(nota)
        
        if len(dado_error) > 0:
            texto_feedback.configure(text=f'Não foi possível alterar essas notas: {dado_error}', text_color='red')
        else:
            texto_feedback.configure(text='notas alteradas com sucesso!!', text_color='green')
    
    def deletar(self,nota: Nota) -> None:
        self.service.deletar(nota)

    def pesquisar(self, pesquisa: str, categoria: str):
        pass

if __name__ == '__main__':
    pass
