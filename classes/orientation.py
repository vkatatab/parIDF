# -*- coding: utf-8 -*-
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
