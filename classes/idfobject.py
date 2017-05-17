# -*- coding: utf-8 -*-
# Esse arquivo é um modelo de uma classe do arquivo IDF
# A classe contém:
#   - Nome (Nome da classe)
#   - Identificador (Nome do paramêtro que identifica a unicidade da classe)
#   - Parâmetros

# imports : importa as classes necessárias
import re
import collections

# Classe no sistema que represta a classe do IDF
class IDFObject(object):
    # Construtor do objeto recebe como parâmetro uma string da classe do IDF
    # Esse método é responsável por analisar o objeto IDF e definir as váriaveis correspondentes
    def __init__(self, string):
        self.string = string
        self.idfObjectLines = []
        self.parameters = collections.OrderedDict()
        self.idfClass = ''
        self.identifier = ''
        self.separateLines()
        self.setIdentifier()
        self.setIdfClass()
        self.convertLinesToParameters()

    # Retorna um paramêtro dado um nome
    def getParameterByName(self, name):
        return self.parameters[name]

    # Modifica um paramêtro dado um nome e um valor
    def setParameterByName(self, name, value):
        self.parameters[name] = value

    # Converta cada linha do arquivo IDF em um parâmetro
    def convertLinesToParameters(self):
        for line in self.idfObjectLines:
            self.parameters[self.getParameterName(line).strip()] = self.getParameterValue(line).strip()

    # Em uma única linha esse método é responsável por retornar o nome do parâmetro
    def getParameterName(self, string):
        position = string.find('!-') + 2
        name = string[position:]
        return name

    # Em uma única linha esse método é responsável por retornar o valor do parâmetro
    def getParameterValue(self, string):
        regex = re.search('(.+)[,;]', string)
        found = ''
        if regex:
            found = regex.group(1)
        return found

    # Método responsável por dizer qual é o identificador dessa classe IDF
    def setIdentifier(self):
        self.identifier = self.getParameterName(self.idfObjectLines[1])

    # Retorna o nome do parâmetro identificador
    def getIdentifier(self):
        return self.identifier

    def __len__(self):
        return 1;

    # Método responsável por separar as linhas da string da classe IDF em variáveis
    def separateLines(self):
        for line in ''.join(self.string).splitlines():
            self.idfObjectLines.append(line)

    # Identifica e seta o nome da classe do IDF
    def setIdfClass(self):
        teste = self.idfObjectLines[0].strip(',')
        self.idfClass = teste
        del self.idfObjectLines[0]

    # Retorna o nome da classe do IDF
    def getIdfClass(self):
        return self.idfClass

    # Retorna todos os parâmetros da classe IDF
    def getParameters(self):
        return self.parameters

    # Retorna a string da classe IDF
    def getString(self):
        return self.string

    # Método responsável por recriar a string do IDF, com os parâmetros atuais
    def getObjectString(self):
        string = self.getIdfClass() + ',\n\r'
        countParameters = len(self.parameters)
        counter = 1
        for (name, parameter) in self.parameters.items():
            spaces = self.getSpaces(parameter)
            if (counter == countParameters):
                string += '    ' + parameter + ';' + spaces + '!- ' + name  + '\n'
            else:
                string += '    ' + parameter + ',' + spaces + '!- ' + name  + '\n'
            counter += 1
        return string

    # Método para organizar as linhas do IDF
    def getSpaces(self, parameter):
        quantity = 30 - len(parameter) + 4
        string = ""
        if (quantity < 0):
            quantity = 2
        for x in range(0,quantity):
            string += " "
        return string
