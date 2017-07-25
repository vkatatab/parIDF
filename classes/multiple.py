# -*- coding: utf-8 -*-
# Essa classe Multiple é um teste de um algotimo que pode ser utilizado para as variações dos parâmetros
import random
import math

class Multiple(object):

    def __init__(self, parameters):
        self.newValue = 0
        self.newValue = float(parameters) * 2

    def getNewValue(self):
        return str(self.newValue)
