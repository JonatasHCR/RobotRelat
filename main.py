'''
main.py

modulo principal do projeto fazendo a execução do projeto

'''
from config.settings import criar_env

criar_env()

from app.view.view import App
from app.controller.controller_relatorio import ControllerRelatorio

App(ControllerRelatorio())
