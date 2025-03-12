import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0,PROJECT_ROOT)

import openpyxl
from openpyxl.styles import NamedStyle,Alignment,Font
from model.model import ModelPro
from utils.utils import UtilsPro
from datetime import datetime

class RelatorioPro:
    def __init__(self):
        self.utils = UtilsPro()

    
    def mensal(self, dados_mes: list[ModelPro], dados_all: list[ModelPro], data_atual: datetime):
        self.workbook = openpyxl.Workbook()

        # Criando um estilo para dinheiro (R$)
        self.real_style = NamedStyle(name="real_style")
        self.real_style.number_format = '"R$"#,##0.00'  # Formato de moeda
        self.workbook.add_named_style(self.real_style)
        
        self.planilha = self.workbook.active
        self.planilha.title = 'Previsão de Faturamento'

        

        mes = self.utils.MESES[dados_mes[0].mes_ref]
        ano = dados_mes[0].ano_ref
        mes_anterior = self.utils.MESES[dados_mes[0].mes_ref - 1]
        comparar_ano_anterior = dados_mes[0].mes_ref == 0
        
        nome = f'Relatorio_{mes}_{ano}.xlsx'

        linha_atual = self.planilha.min_row
        self.planilha.merge_cells(f'A{linha_atual}:F{linha_atual}')
        self.planilha[f'A{linha_atual}'].value = f'Previsão de Faturamento {mes}/{ano}'.upper()
        self.planilha[f'A{linha_atual}'].alignment = Alignment(horizontal="center")
        self.planilha[f'A{linha_atual}'].font = Font(bold=True)

        self.planilha.append(self.utils.colunas_all_planilha)
        linha_atual = self.planilha.max_row
        coluna_inicio = self.planilha.min_column
        coluna_fim = self.planilha.max_column
        self.utils.style_font_planilha(self.planilha,linha_atual,linha_atual, coluna_inicio,coluna_fim)
        
        linha_atual = self.planilha.max_row
        faturado = 0
        nao_faturado = 0
        for dado in dados_mes:
            valor_cc_pago = 0
            valor_cc_faturado = 0
            valor_cc_nao_faturado = 0
            lista = set()
            for data_fat,data_pag,valor in zip(dado.data_fat.split(','),dado.data_pag.split(','),dado.valor.split(',')):
                
                valor = float(valor)
                if data_fat == '':
                    valor_cc_nao_faturado += valor
                    nao_faturado += valor
                    lista.add(('-','-')) 
                    continue
                
                if data_pag != '' :
                    faturado += valor
                    data_pag = datetime.strptime(data_pag,"%Y-%m-%d")
                    if data_pag > data_atual:
                        valor_cc_faturado += valor
                        lista.add(('SIM','-')) 
                    else:
                        valor_cc_pago += valor
                        lista.add(('SIM','SIM')) 
                else:
                    faturado += valor
                    valor_cc_faturado += valor
                    lista.add(('SIM','-'))

            for data_fat,data_pag in lista:
                dado.data_fat = data_fat
                dado.data_pag = data_pag

                match data_fat+data_pag:
                    case '--':
                        dado.valor = valor_cc_nao_faturado
                        dado_nul = dado.__dict__.copy()
                        
                        dado_nul.pop('tipo')
                        dado_nul.pop('mes_ref')
                        dado_nul.pop('ano_ref')
                        self.planilha.append(list(dado_nul.values()))
                    
                    case 'SIM-':
                        dado.valor = valor_cc_faturado
                        dado_faturado = dado.__dict__.copy()
                        
                        dado_faturado.pop('tipo')
                        dado_faturado.pop('mes_ref')
                        dado_faturado.pop('ano_ref')
                        self.planilha.append(list(dado_faturado.values()))
                    
                    case "SIMSIM":
                        dado.valor = valor_cc_pago
                        dado_pago = dado.__dict__.copy()
                        
                        dado_pago.pop('tipo')
                        dado_pago.pop('mes_ref')
                        dado_pago.pop('ano_ref')
                        self.planilha.append(list(dado_pago.values()))
        
        linha_final = self.planilha.max_row
        self.planilha.append(['\n'])
        self.planilha.append(['FATURADO', faturado])
        self.planilha.append(['A FATURAR', nao_faturado])
        self.planilha.append(['TOTAL',f"=SUM(B{linha_atual+1}:B{linha_final})"])
        
        linha_final = self.planilha.max_row
        self.utils.style_real_planilha(self.planilha,linha_atual+1,linha_final, 2,2, self.real_style)
        self.utils.style_alinhar_planilha(self.planilha,linha_atual+1,linha_final, 3,5)
        self.utils.style_font_planilha(self.planilha,linha_final-2,linha_final, coluna_inicio,2)
        self.utils.style_borda_planilha(self.planilha,1,linha_final, coluna_inicio,coluna_fim)

        self.planilha.append(['\n'])

        linha_atual = self.planilha.max_row + 1

        self.planilha.merge_cells(f'A{linha_atual}:F{linha_atual}')
        if comparar_ano_anterior:
            self.planilha[f'A{linha_atual}'].value = f'Faturamento Meses Anteriores {mes_anterior}/{ano - 1}'.upper()
        else:
            self.planilha[f'A{linha_atual}'].value = f'Faturamento Meses Anteriores {mes_anterior}/{ano}'.upper()

        self.planilha[f'A{linha_atual}'].alignment = Alignment(horizontal="center")
        self.planilha[f'A{linha_atual}'].font = Font(bold=True)

        self.planilha.append(self.utils.colunas_all_planilha)
        
        linha_atual = self.planilha.max_row
        self.utils.style_font_planilha(self.planilha,linha_atual,linha_atual, coluna_inicio,coluna_fim)

        for dado in dados_all:
            valor_cc_pago = 0
            valor_cc_faturado = 0
            lista = set()
            for data_fat,data_pag,valor in zip(dado.data_fat.split(','),dado.data_pag.split(','),dado.valor.split(',')):
                
                valor = float(valor)
                if data_fat == '':
                    continue
                
                if data_pag != '' :
                    data_pag = datetime.strptime(data_pag,"%Y-%m-%d")
                    if data_pag.month - 1 == self.utils.MESES.index(mes):
                        valor_cc_pago += valor
                        lista.add(('SIM','SIM'))
                        
                else:
                    valor_cc_faturado += valor
                    lista.add(('SIM','-'))

            for data_fat,data_pag in lista:
                dado.data_fat = data_fat
                dado.data_pag = data_pag

                match data_fat+data_pag:
                    
                    case 'SIM-':
                        dado.valor = valor_cc_faturado
                        dado_faturado = dado.__dict__.copy()
                        
                        dado_faturado.pop('tipo')
                        dado_faturado.pop('mes_ref')
                        dado_faturado.pop('ano_ref')
                        self.planilha.append(list(dado_faturado.values()))
                    
                    case "SIMSIM":
                        dado.valor = valor_cc_pago
                        dado_pago = dado.__dict__.copy()
                        
                        dado_pago.pop('tipo')
                        dado_pago.pop('mes_ref')
                        dado_pago.pop('ano_ref')
                        self.planilha.append(list(dado_pago.values()))
        
        linha_final = self.planilha.max_row
        self.planilha.append(['\n'])  
        self.planilha.append(['TOTAL',f"=SUM(B{linha_atual+1}:B{linha_final})"])
        linha_final = self.planilha.max_row
        
        self.utils.style_real_planilha(self.planilha,linha_atual+1,linha_final, 2,2, self.real_style)
        self.utils.style_alinhar_planilha(self.planilha,linha_atual+1,linha_final, 3,5)
        self.utils.style_font_planilha(self.planilha,linha_final,linha_final, coluna_inicio,2)
        self.utils.style_borda_planilha(self.planilha,linha_atual-1,linha_final, coluna_inicio,coluna_fim)
        
        self.utils.ajustar_colunas_planilha(self.planilha)
        
        nome = f'Relatorio_{mes}_{ano}.xlsx'

        self.workbook.save(nome)







        


        