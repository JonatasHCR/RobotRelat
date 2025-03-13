'''
main.py

modulo principal do projeto fazendo a execução do projeto

'''
import config
from view.view import App
from controller.controller import ControllerPro

App(ControllerPro())
