'''
main.py

modulo principal do projeto fazendo a execução do projeto

'''
from config.settings import criar_env
from view.view import App
from controller.controller import ControllerPro

criar_env()
App(ControllerPro())
