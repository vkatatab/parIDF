import re

# (.+),[\n\r]((.+)[,;]\s*!-.+\n)+

class IDFObject(object):
    def __init__(self, string):
        self.string = string
        self.idfObjectLines = []
        self.parameters = {}
        self.idfClass = ''
        self.separateLines()
        self.setIdfClass()
        self.convertLinesToParameters()

    def toString(self):
        string = self.getName() + ','

    def getParameterByClass(self, name):
        return self.parameters[name]

    def setParameterByClass(self, name, value):
        self.parameters[name] = value

    def convertLinesToParameters(self):
        for line in self.idfObjectLines:
            self.parameters[self.getParameterName(line).strip()] = self.getParameterValue(line).strip()

    def getParameterName(self, string):
        position = string.find('!-') + 2
        name = string[position:]
        return name

    def getParameterValue(self, string):
        regex = re.search('(.+)[,;]', string)
        found = ''
        if regex:
            found = regex.group(1)
        return found

    def separateLines(self):
        for line in self.string.splitlines():
            self.idfObjectLines.append(line)

    def setIdfClass(self):
        teste = self.idfObjectLines[0].strip(',')
        self.idfClass = teste
        del self.idfObjectLines[0]

    def getIdfClass(self):
        return self.idfClass

    def getParameters(self):
        return self.parameters

    def getString(self):
        return self.string