# -*- coding: utf-8 -*-
import random
import math

class Multiple(object):

    def __init__(self, parameters):
        self.newValue = 0
        self.newValue = float(parameters) * 2

    def getNewValue(self):
        return str(self.newValue)
