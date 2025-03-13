'''
nota.py

modulo que estará contendo a classe que representa a tabela
notas do banco de dados, tendo suas colunas como atributos.

'''

class ModelNota:
    """
    Classe da aplicação, responsável representar a tabela notas
    do banco de dados
    
    A classe inicializa os atributos que estão referenciando as colunas
    e coloca seus respectivos valores
    """

    def __init__(self,id: int, centro_de_custo: str, numero_nota: str, valor_nota: float, data_fat: str, data_pag: str, mes_ref: int, ano_ref: int) -> None:
        '''
        Inicializa criando os atributos relacionado as colunas, 
        e colocando já os valores

        param: 
            id (int): Identificação da conjunto de dados 
            centro_de_custo (str): Centro de custo relacionado a nota 
            numero_nota (str): Numero da nota fiscal 
            valor_nota (float): Valor da nota fiscal 
            data_fat (str): Data de faturamento da nota 
            data_pag (str): Data de pagamento da nota 
            mes_ref (int): Mês de referencia, mês que ela foi emitida 
            ano_ref (int): Ano de referencia, ano que ela foi emitida

        '''
        
        self.id = id
        self.cc = centro_de_custo
        self.numero_nota = numero_nota
        self.valor_nota = valor_nota
        self.data_fat = data_fat
        self.data_pag = data_pag
        self.mes_ref = mes_ref
        self.ano_ref = ano_ref

    def __str__(self):

        return f"{self.cc}|{self.numero_nota}|R$ {str(self.valor_nota).replace('.',',')}|{self.data_fat}|{self.data_pag}|{self.mes_ref}|{self.ano_ref}"
    