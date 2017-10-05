# -*- coding: utf-8 -*-
# Essa classe MonteCarlo é o algoritmo responsavel por gerar as variações randomicas dos parâmetros

import random
import math

class Overhang4(object):

    def __init__(self, parameters):
        self.newValue = 0;
        orientation = int(parameters)
        precision = 0.01
        minNumber = 0.01
        maxNumber = 0.01
        if (orientation == 0):
            maxNumber = 2.75
        elif (orientation == 45):
            maxNumber = 2.75
        elif (orientation == 90):
            maxNumber = 1.73
        elif (orientation == 135):
            maxNumber = 2.75
        elif (orientation == 180):
            maxNumber = 2.75
        elif (orientation == 225):
            maxNumber = 1.19
        elif (orientation == 270):
            maxNumber = 0.36
        elif (orientation == 315):
            maxNumber = 1.19

        rand = random.randint(0,math.floor((maxNumber - minNumber)/precision))
        self.newValue = round ((rand * precision) + minNumber, 2)

    def getNewValue(self):
        return str(self.newValue)
