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
from model.banco import DatabasePro
from config.utils import UtilsPro

#importação para a tipagem
from customtkinter import CTkLabel

class ControllerPro:
    """
    Classe responsável pelo controle das operações do sistema financeiro.

    Atua como intermediária entre a interface gráfica e o banco de dados,
    realizando operações como cadastro, modificação e recuperação de clientes e notas fiscais.
    """

    def __init__(self):
        """
        Inicializa a classe ControllerPro.
        
        Cria instâncias das classes DatabasePro e UtilsPro.
        """
        self.db = DatabasePro()
        self.utils = UtilsPro()

    def cadastrar_nota(self, texto_feedback: CTkLabel, dicionario: dict) -> None:
        """
        Cadastra uma nota fiscal no banco de dados.

        param:
            texto_feedback(CTkLabel): Label para exibir mensagens de feedback ao usuário.
            dicionario(dict): Dicionário contendo os dados da nota a serem cadastrados.
        """
        try:
            dados_formatados = self.utils.formatar_dados(dicionario)
        except ValueError:
            texto_feedback.configure(text='Erro ao cadastrar valor não informado', text_color='red')
            return
        
        quant = int(dicionario["Quantidade de Registros"].get())

        #pegando os dados ja formatados
        centro_custo = dados_formatados['Centro de Custo']
        numero_nota = dados_formatados['Numero da Nota']
        valor_nota = dados_formatados['Valor da Nota']
        data_fat = dados_formatados['Data de Faturamento']
        data_pag = dados_formatados['Data de Pagamento']
        mes_ref = dados_formatados["Mês de Referência"]
        ano_ref = dados_formatados['Ano de Referência']

        if not self.db.verificar_centro_custo(centro_custo):
            texto_feedback.configure(text='Erro ao cadastrar centro de custo não existe', text_color='red')
            return

        try:
            self.db.inserir_nota(centro_custo,numero_nota,valor_nota,data_fat,data_pag,mes_ref,ano_ref)
            texto_feedback.configure(text='Nota cadastrada com sucesso!!', text_color='green')
            self.utils.apagar_valores(dicionario,quant,nota=True)
        except IntegrityError:
            texto_feedback.configure(text='Erro ao cadastrar nota', text_color='red')

    def cadastrar_cliente(self, texto_feedback: CTkLabel, dicionario: dict) -> None:
        """
        Cadastra um cliente no banco de dados.

        param:
            texto_feedback(CTkLabel): Label para exibir mensagens de feedback ao usuário.
            dicionario(dict): Dicionário contendo os dados do cliente a serem cadastrados.
        """
        dados_formatados = self.utils.formatar_dados(dicionario)

        quant = int(dicionario["Quantidade de Registros"].get())
        
        #pegando os dados ja formatados
        cliente = dados_formatados['Cliente']
        centro_custo = dados_formatados['Centro de Custo']
        descricao = dados_formatados['Descrição']
        tipo = dados_formatados["Tipo de Cliente"]

        if centro_custo == '':
            texto_feedback.configure(text='Centro de custo está vazio', text_color='red')
            return

        try:
            self.db.inserir_cliente(cliente,centro_custo,descricao,tipo)
            texto_feedback.configure(text='Cliente cadastrado com sucesso!!', text_color='green')
            self.utils.apagar_valores(dicionario,quant,cliente=True)
        except IntegrityError:
            texto_feedback.configure(text='Centro de custo já cadastrado', text_color='red')

    def retirar_clientes(self, pagina: int) -> list[list]:
        """
        Recupera a lista de clientes cadastrados.

        param:
            pagina(int): Número da página de registros a ser recuperada.
        return: 
            (list[list]): Lista contendo a lista de dados dos clientes.
        """
        return self.db.retirar_clientes(pagina)

    def contar_pagina(self, cliente: bool = False, notas: bool = False, all: bool = False) -> int:
        """
        Conta o número de páginas disponíveis para clientes, notas ou todos os registros.

        param:
            cliente(bool): Se True, conta páginas de clientes.
            notas(bool): Se True, conta páginas de notas fiscais.
            all(bool): Se True, conta todas as páginas de registros.
        return: 
            (int): Número total de páginas.
        """
        return self.db.contar_pagina(cliente=cliente, notas=notas, all=all)

    def retirar_notas(self, pagina: int) -> list[list]:
        """
        Recupera a lista de notas fiscais cadastradas.

        param: 
            pagina(int): Número da página de registros a ser recuperada.
        return: 
            (list[list]): Lista contendo a lista de dados das notas fiscais.
        """
        return self.db.retirar_notas(pagina, remove_id=False)

    def retirar_all(self, pagina: int) -> list[list]:
        """
        Recupera todos os registros disponíveis.

        param: 
            pagina(int): Número da página de registros a ser recuperada.
        
        return: 
            (list[list]): Lista contendo a Lista de dados mescados dos clientes e notas.
        """
        return self.db.retirar_all(pagina)

    def modificar_cliente(self, dados: list[dict], texto_feedback: CTkLabel) -> None:
        """
        Modifica os dados de clientes cadastrados.

        param:
            dados(list[dict]): Lista de dicionários contendo os novos dados dos clientes.
            texto_feedback(CTkLabel)): Label para exibir mensagens de feedback ao usuário.
        """
        dado_error = []
        for dado in dados:
            
            dado_formatado = self.utils.formatar_dados(dado)
            
            #pegando os dados ja formatados
            cliente = dado_formatado['Clientes']
            centro_custo = dado_formatado["Centro de Custo"]
            descricao = dado_formatado["Descrição"]
            tipo = dado_formatado["Tipo"]
            centro_custo_velho = dado_formatado['Centro de Custo Velho']

            if centro_custo == '':
                dado_error.append(dado_formatado)
                texto_feedback.configure(text=f'Não foi possível alterar desses: {dado_error}', text_color='red')
                continue
            try:
                self.db.modificar_cliente(cliente,centro_custo,descricao,tipo,centro_custo_velho)
                texto_feedback.configure(text='Clientes alterados com sucesso!!', text_color='green')
            except IntegrityError:
                dado_error.append(dado_formatado)
                texto_feedback.configure(text=f'Não foi possível alterar esses clientes: {dado_error}', text_color='red')

    def modificar_nota(self, dados: list[dict], texto_feedback: CTkLabel) -> None:
        """
        Modifica os dados de notas fiscais cadastradas.

        param:
            dados(list[dict]): Lista de dicionários contendo os novos dados das notas.
            texto_feedback(CTkLabel): Label para exibir mensagens de feedback ao usuário.
        """
        dado_error = []
        for dado in dados:
            try:
                dado_formatado = self.utils.formatar_dados(dado)
            except ValueError:
                dado_error.append(dado_formatado)
                texto_feedback.configure(text=f'Erro ao alterar essas notas: {dado_error}', text_color='red')
                continue
            
            #pegando os dados ja formatados
            id_nota =  int(dado_formatado['id'])
            centro_custo = dado_formatado["Centro de Custo"]
            numero_nota = dado_formatado["Numero da Nota"]
            valor_nota = dado_formatado["Valor da Nota"]
            data_fat = dado_formatado["Data de Faturamento"]
            data_pag = dado_formatado["Data de Pagamento"]
            mes_ref = dado_formatado["Mês de Referência"]
            ano_ref = dado_formatado["Ano de Referência"]

            if centro_custo == '':
                dado_error.append(dado_formatado)
                texto_feedback.configure(text=f'Erro ao alterar essas notas: {dado_error}', text_color='red')
                continue
           
            if not self.db.verificar_centro_custo(centro_custo):
                dado_error.append(dado_formatado)
                texto_feedback.configure(text=f'Erro ao alterar essas notas: {dado_error}', text_color='red')
                continue
            
            try:
                self.db.modificar_nota(id_nota,centro_custo,numero_nota,valor_nota,data_fat,data_pag,mes_ref,ano_ref)
                texto_feedback.configure(text='Notas alteradas com sucesso!!', text_color='green')

            except IntegrityError:
                dado_error.append(dado_formatado)
                texto_feedback.configure(text=f'Erro ao alterar essas notas: {dado_error}', text_color='red')

    def pesquisar(self, pesquisa: str, categoria: str):
        pass

if __name__ == '__main__':
    pass
