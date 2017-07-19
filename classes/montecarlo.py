# -*- coding: utf-8 -*-
import random
import math

class MonteCarlo(object):

    def __init__(self, parameters):
        self.newValue = 0;
        mini = parameters['min']
        maxi = parameters['max']
        precision = parameters['precision']
        rand = random.randint(0,math.floor((maxi - mini)/precision))
        self.newValue = (rand * precision) + mini

    def getNewValue(self):
        return str(round (self.newValue, 2))
