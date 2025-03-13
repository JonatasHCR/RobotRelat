class ModelPro:
    """
    Classe da aplicação, responsável representar um modelo de relatório
    não presente no banco de dados
    
    A classe inicializa os atributos que estão referenciando o modelo
    de relatório coloca seus respectivos valores
    """

    def __init__(self, nome: str,tipo: str, valor: float|str, centro_de_custo: str, data_fat: str, data_pag: str, descricao: str, mes_ref: int, ano_ref: int) -> None:
        '''
        Inicializa criando os atributos relacionado ao modelo, 
        e colocando já os valores

        param: 
            nome (str): Nome do cliente 
            tipo (str): Tipo do cliente(Próprio ou Consorcio)
            valor_nota (float): Valor da nota fiscal
            centro_de_custo (str): Centro de custo relacionado ao cliente
            data_fat (str): Data de faturamento da nota 
            data_pag (str): Data de pagamento da nota
            descricao (str): Um resumo do cliente
            mes_ref (int): Mês de referencia, mês que ela foi emitida 
            ano_ref (int): Ano de referencia, ano que ela foi emitida 

        '''

        self.nome = nome
        self.tipo = tipo
        self.valor = valor
        self.cc = centro_de_custo
        self.data_fat = data_fat
        self.data_pag = data_pag 
        self.descricao = descricao
        self.mes_ref = mes_ref
        self.ano_ref = ano_ref
    
    def __str__(self):
        '''
        Retornara todos os valores separados por "|"
        '''
        return f"{self.nome}|{self.tipo}|R$ {str(self.valor_nota).replace('.',',')}|{self.cc}|{self.data_fat}|{self.data_pag}|{self.descricao}"