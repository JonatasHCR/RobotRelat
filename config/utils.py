'''
utils.py

modulo que estará contendo a classe com funções auxiliares,
listas, entre outras ajudas para o projeto.

'''

from datetime import datetime
import customtkinter as ctk

class UtilsPro:
    """
    Classe utilitária para manipulação e formatação de dados em um sistema de gerenciamento financeiro.

    Contém métodos para formatação de valores monetários, manipulação de datas, limpeza de formulários,
    controle de tela cheia, entre outras funções auxiliares.
    """

    def __init__(self) -> None:
        """
        Inicializa a classe com listas de meses, colunas de dados e tipos de clientes.
        """
        self.MESES = [
            'JANEIRO', 'FEVEREIRO', 'MARÇO', 'ABRIL', 'MAIO', 'JUNHO', 
            'JULHO', 'AGOSTO', 'SETEMBRO', 'OUTUBRO', 'NOVEMBRO', 'DEZEMBRO'
        ]

        self.colunas_clientes = ['Clientes', "Centro de Custo", "Tipo", "Descrição"]

        self.colunas_notas = [
            "Centro de Custo", "Numero da Nota", "Valor da Nota", "Data de Faturamento", 
            "Data de Pagamento", "Mês de Referência", "Ano de Referência"
        ]

        self.colunas_all = [
            'Clientes', "Tipo", "Valor da Nota", "Centro de Custo", 
            "Data de Faturamento", "Data de Pagamento", "Descrição"
        ]

        self.tipo_cliente = ["Consórcio", "Próprio"]

    def formatar_dados(self, dicionario: dict) -> dict:
        """
        Formata os valores de um dicionário, convertendo datas e valores monetários.

        param:
            dicionario(dict): Dicionário contendo os dados a serem formatados.
        
        return
            (dict): Dicionário com os dados formatados.
        """
        dict_dados = dict()

        for chave, dado in dicionario.items():
            dado = str(dado.get())#pegando o dado do campo de entrada
    
            match chave:
                case 'Valor da Nota':
                    dinheiro = self.formatar_dinheiro(dado)
                    dict_dados[chave] = dinheiro
                case 'Data de Faturamento' | 'Data de Pagamento':
                    data = self.formatar_data(dado)
                    dict_dados[chave] = data
                case _:
                    dict_dados[chave] = dado.strip()

        return dict_dados

    def formatar_dinheiro(self, dinheiro: str) -> float:
        """
        Converte uma string representando dinheiro em um valor float.

        param:
            dinheiro(str): String representando um valor monetário (ex: "R$1.234,56").
        
        return: 
            (float): Valor convertido para float.
        
        raises 
            ValueError: Se a conversão falhar.
        """
        valor = dinheiro.strip()
        try:
            valor = valor.replace('R$', '').replace('.', '').replace(',', '.')
            return float(valor.strip())
        except ValueError:
            raise ValueError("Erro ao converter valor")

    def formatar_data(self, data: str) -> str:
        """
        Converte uma data no formato brasileiro para o formato internacional (YYYY-MM-DD) e vice-versa.

        param:
            data(str): String representando uma data (ex: "10/05/2023" ou "2023-05-10").
        
        return: 
            (str): Data formatada como string.
        """
        data_for = data

        try:
            if data_for:
                data_for = data_for.split('/')
                data_for = datetime(
                    day=int(data_for[0]), month=int(data_for[1]), year=int(data_for[2])
                ).strftime("%Y-%m-%d")
        except ValueError:
            data_for = data.split('-')
            data_for = datetime(
                int(data_for[0]), int(data_for[1]), int(data_for[2])
            ).strftime("%d/%m/%Y")
            return self.formatar_data(data_for)

        return data_for

    def apagar_valores(self, dicionario: dict, quant: int, cliente: bool = False, nota: bool = False) -> None:
        """
        Limpa os valores dos campos de entrada conforme a quantidade de registros.

        param:
            dicionario(dict): Dicionário contendo os campos de entrada.
            quant(int): Quantidade de registros.
            cliente(bool): Se True, limpa campos relacionados a clientes.
            nota(bool): Se True, limpa campos relacionados a notas fiscais.
        """
        for chave, dado in dicionario.items():
            match chave:
                case 'Ano de Referência':
                    if quant == 1:
                        dado.delete(0, 'end')
                        dado.insert(0, str(self.pegar_ano_atual()))
                case "Mês de Referência":
                    if quant == 1:
                        dado.set(self.MESES[self.pegar_mes_atual()])
                case "Quantidade de Registros":
                    if quant > 1:
                        dado.set(str(quant - 1))
                case "Tipo de Cliente":
                    continue
                case 'Centro de Custo':
                    if quant > 1 and nota:
                        continue
                    elif cliente:
                        dado.delete(0, 'end')
                    else:
                        dado.delete(0, 'end')
                case _:
                    if quant == 1 or nota:
                        dado.delete(0, 'end')

    def limpar(self, janela: ctk.CTk) -> None:
        """
        Remove todos os widgets da janela, exceto os primeiros botões principais.

        param 
            janela(CTk): A janela de onde os widgets serão removidos.
        """
        contador = 0
        for componente in janela.winfo_children():
            if isinstance(componente, (ctk.CTkLabel, ctk.CTkEntry)):
                componente.destroy()
            elif contador > 3 and isinstance(componente, (ctk.CTkButton, ctk.CTkComboBox)):
                componente.destroy()

            contador += 1

    def sair_fullscreen(self, janela: ctk.CTk) -> None:
        """
        Sai do modo tela cheia e limpa a interface.

        param 
            janela(CTk): A janela que sairá do modo fullscreen.
        """
        janela.attributes("-fullscreen", False)
        self.limpar(janela)

    def entrar_fullscreen(self, janela: ctk.CTk, coluna: int, linha: int) -> None:
        """
        Entra no modo tela cheia e adiciona um botão para sair desse modo.

        param:
            janela(CTk): A janela que entrará em tela cheia.
            coluna(int): Posição da coluna para o botão de saída.
            linha(int): Posição da linha para o botão de saída.
        """
        janela.attributes("-fullscreen", True)
        botao_sair = ctk.CTkButton(janela, text="Sair do Fullscreen", command=lambda: self.sair_fullscreen(janela))
        botao_sair.grid(column=coluna, row=linha, pady=10, padx=10)

    def pegar_mes_atual(self) -> int:
        """
        Retorna o índice do mês atual (baseado em zero, onde janeiro é 0 e dezembro é 11).

        return: 
            (int): Índice do mês atual.
        """
        return datetime.now().month - 1

    def pegar_ano_atual(self) -> int:
        """
        Retorna o ano atual.

        return: 
            (int): Ano atual como inteiro.
        """
        return datetime.now().year
if __name__ == '__main__':
    #inicio()
    print(UtilsPro().MESES)