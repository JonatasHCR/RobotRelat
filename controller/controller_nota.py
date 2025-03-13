'''
controller_nota.py

modulo que estará contendo a classe que faz a ponte entre a parte
gráfica, e a resposta do service relacionado ao nota.

'''

#importações para que consiga importar desde a raiz do projeto
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0,PROJECT_ROOT)

#importações para funcionamento da classe
from model.model_nota import ModelNota
from service.service_nota import ServiceNota
from utils.utils import UtilsPro

#importando o erro
from sqlite3 import IntegrityError

#importação para a tipagem
from customtkinter import CTkLabel,CTkEntry

class ControllerNota:
    """
    Classe responsável pelo controle das operações do sistema financeiro.

    Atua como intermediária entre a interface gráfica e o service que
    realiza operações como cadastro, modificação e recuperação de notas fiscais.
    """

    def __init__(self):
        """
        Inicializa a classe ControllerPro.
        
        Cria instâncias das classes ServiceNota e UtilsPro.
        """
        self.service = ServiceNota()
        self.utils = UtilsPro()

    def cadastrar(self, texto_feedback: CTkLabel, dicionario: dict) -> None:
        """
        Aciona o service para cadastrar a nota no banco de dados.

        param:
            texto_feedback(CTkLabel): Label para exibir mensagens de feedback ao usuário.
            dicionario(dict[str,CTkEntry]): Dicionário contendo os dados da nota a serem cadastrados.
        """

        #pegando a quantidade de registros que é pra ser feito
        quant = int(dicionario["Quantidade de Registros"].get())

        #pegando os dados das entrys
        centro_custo = dicionario['Centro de Custo'].get()
        numero_nota = dicionario['Numero da Nota'].get()
        valor_nota = dicionario['Valor da Nota'].get()
        data_fat = dicionario['Data de Faturamento'].get()
        data_pag = dicionario['Data de Pagamento'].get()
        mes_ref = dicionario["Mês de Referência"].get()
        ano_ref = dicionario['Ano de Referência'].get()

        #criando a instancia com os dados
        nota = ModelNota('',centro_custo,numero_nota,valor_nota,data_fat,data_pag,mes_ref,ano_ref)

        #verificando se os dados estão corretos
        try:
            #acionando o service pra tentar inserir 
            self.service.inserir(nota)

            #dando o resultado do cadastro pro usuário
            texto_feedback.configure(text='Nota cadastrada com sucesso!!', text_color='green')

            #limpando ou não as entrys
            self.utils.apagar_valores(dicionario,quant,nota=True)
        except:
            #dando o resultado do cadastro pro usuário
            texto_feedback.configure(text='Erro ao cadastrar nota', text_color='red')

    def contar_pagina(self) -> int:
        """
        Aciona o service para contar o número 
        de páginas disponíveis para nota

        return: 
            (int): Número total de páginas.
        """
        return self.service.paginas()

    def retirar(self, pagina: int) -> list[ModelNota]:
        """
        Aciona o service para recuperar a 
        lista das notas cadastradas.

        param:
            pagina(int): Número da página de registro a ser recuperada.
        return: 
            (list[ModelNota]): Lista contendo os dados 
            em instâncias do modelo nota
        """
        return self.service.retirar(pagina)


    def modificar(self, dados: list[dict[str,CTkEntry]], texto_feedback: CTkLabel) -> None:
        """
        Aciona o service para modificar 
        os dados das notas cadastradas.

        param:
            dados(list[dict[str,CTkEntry]]): Lista de dicionários contendo os novos dados das notas.
            texto_feedback(CTkLabel)): Label para exibir mensagens de feedback ao usuário.
        """
        dado_error = []
        for dado in dados:

            #pegando os dados das entrys
            id_nota =  int(dado['id'].get())
            centro_custo = dado["Centro de Custo"].get()
            numero_nota = dado["Numero da Nota"].get()
            valor_nota = dado["Valor da Nota"].get()
            data_fat = dado["Data de Faturamento"].get()
            data_pag = dado["Data de Pagamento"].get()
            mes_ref = dado["Mês de Referência"].get()
            ano_ref = dado["Ano de Referência"].get()

            #criando a instancia com os dados
            nota = ModelNota(id_nota,centro_custo,numero_nota,valor_nota,data_fat,data_pag,mes_ref,ano_ref)
            
            #verificando se os dados estão corretos
            try:
                #acionando o service pra tentar modificar
                self.service.modificar(nota)

            except (IntegrityError,ValueError):
                #caso erro acrescentando qual modificação deu erro
                dado_error.append(nota)
        
        #verificando se teve dados que deram erro
        if len(dado_error) > 0:
            texto_feedback.configure(text=f'Não foi possível alterar essas notas: {dado_error}', text_color='red')
        else:
            texto_feedback.configure(text='notas alteradas com sucesso!!', text_color='green')
    
    def deletar(self,nota: ModelNota) -> None:
        """
        Aciona o service para deletar 
        a nota do banco.

        param:
            nota (ModelNota): nota que vai ser deletada
        """
        self.service.deletar(nota)

    def pesquisar(self, pesquisa: str, categoria: str):
        pass
