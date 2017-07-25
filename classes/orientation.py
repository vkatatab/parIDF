# -*- coding: utf-8 -*-
# Essa classe Orientation é utilizada devido a relacao de dependencia entre parametros
# quando é alterada a orientação no energyplus do modelo é necessário alterar juntamente outro parâmetro
# da ventilação natural, no caso de haver o grupo airflownetwork, pois muda os coeficientes de pressão

import random
import math

class Orientation(object):

    def __init__(self, parameters):
        self.newValue = 0
        parameters = int(parameters)
        if (parameters <= 180):
        	self.newValue =  parameters
        else:
        	self.newValue =  parameters - 180

    def getNewValue(self):
        return str(self.newValue)
