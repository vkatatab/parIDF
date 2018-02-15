# -*- coding: utf-8 -*-

class SameNumberValue(object):

    def __init__(self, parameters):
        self.newValue = parameters['value'].split('=')[1].strip()
        if 'text' in parameters:
            self.text = parameters['text']
        else:
            self.text = ''  

    def getNewValue(self):
        value = str(self.newValue)
        if not self.text:
            return value
        return self.text + value

