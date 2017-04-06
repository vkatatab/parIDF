import re

# (.+),[\n\r]((.+)[,;]\s*!-.+\n)+

class IDFObject(object):
    def __init__(self, string):
        self.string = string
        self.idfObjectLines = []
        self.parameters = {}
        self.idfClass = ''
        self.identifier = ''
        self.separateLines()
        self.setIdentifier()
        self.setIdfClass()
        self.convertLinesToParameters()

    def toString(self):
        string = self.getName() + ','

    def getParameterByName(self, name):
        return self.parameters[name]

    def setParameterByName(self, name, value):
        self.parameters[name] = value

    def convertLinesToParameters(self):
        for line in self.idfObjectLines:
            self.parameters[self.getParameterName(line).strip()] = self.getParameterValue(line).strip()

    def getParameterName(self, string):
        position = string.find('!-') + 2
        name = string[position:]
        return name

    def setIdentifier(self):
        self.identifier = self.getParameterName(self.idfObjectLines[1])

    def getIdentifier(self):
        return self.identifier

    def getParameterValue(self, string):
        regex = re.search('(.+)[,;]', string)
        found = ''
        if regex:
            found = regex.group(1)
        return found

    def __len__(self):
        return 1;

    def separateLines(self):
        for line in ''.join(self.string).splitlines():
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

    def getObjectString(self):
        string = self.getIdfClass() + ',\n\r'
        countParameters = len(self.parameters)
        counter = 1
        for (name, parameter) in self.parameters.items():
            if (counter == countParameters):
                string += '\t' + parameter + ';\t\t\t!- ' + name  + '\n\r'
            else:
                string += '\t' + parameter + ',\t\t\t!- ' + name  + '\n\r'
            counter += 1
        return string
