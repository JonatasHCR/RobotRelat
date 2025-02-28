'''
Pacote config

Feito com os principais métodos do projeto envolvendo funções
auxiliares que serão, usadas no projeto, bem como variáveis

Subpacotes:
    utils.py: funções e variáveis, que ajudaram no projeto
'''
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0,PROJECT_ROOT)

from config.settings import criar_pasta_log,criar_env

criar_env()
criar_pasta_log()

