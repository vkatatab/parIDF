# -*- coding: utf-8 -*-
# Essa classe Predifined é utilizada para escolher entre valores fixos randômicos
# ao invés de um intervalo de valores 

import random
import math

class Predefined(object):

    def __init__(self, parameters):
        self.newValue = 0;
        values = parameters['values']
        rand = random.randint(0,len(values)-1)
        self.newValue = values[rand]

    def getNewValue(self):
        return str(self.newValue)
