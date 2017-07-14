# -*- coding: utf-8 -*-
# Este arquivo (main.py) carrega um arquivo de configuração (config.json) que está situado na mesma pasta
# O arquivo de configuração (config.json) fornece os parâmetros e indica as variáveis e valores que serão alterados no idf

# imports : importa as classes necessárias
import sys
import re
import json

# sys.path.insert: possibilita a importação de classes em uma subpasta
sys.path.insert(0, 'classes')

#importação das classes criadas
import idfobject
import idfset
import progressbar
import os

class Main(object):

    def __init__(self, path):
        # inicia a leitura do arquivo de configuração
        fp = open(path)
        file = fp.read()
        self.config = json.loads(file)
        self.parameterFile = self.config['path']['destination'] + '/' + self.config['path']['parameterFile']
        self.wroteHeader = False
        self.header = ''
        self.configString = ''
        if (os.path.isfile(self.parameterFile)):
            os.remove(self.parameterFile)

    def createParameterFile(self, line):
        fp = open(self.parameterFile, 'a')
        fp.write(line)
        fp.write('\n\r')
        fp.close()

    def getNewValueFromConfig(self, alg, parameters, parentValue):
        algName = alg
        module = __import__(algName.lower())
        class_ = getattr(module, algName)
        if ('value' in parameters):
            if (parameters['value'] == 'parent'):
                parameters = parentValue
        instance = class_(parameters)
        return instance.getNewValue()

    def iterateOverClasses(self, idf, items, newValue):
        # itera sobre todas as variáveis configuradas para serem alteradas
        for (classNameChild, classConfig) in items:

            #verifica se a classe não é única, que tem mais de um objeto do idf em uma mesma classe
            if ('identifiers' in classConfig):

                # itera sobre todos os objetos do idf de uma mesma classe
                for (identifier, identifierConfig) in sorted(classConfig['identifiers'].items()):

                    #percorre a configuração preparando para realizar a troca dos valores
                    for (variable, variableConfigChild) in identifierConfig.items():
                        self.alterValue(idf, classNameChild, variable, variableConfigChild, newValue, identifier)

            #caso a clase seja única
            else:
                for (variable, variableConfigChild) in sorted(classConfig.items()):
                    self.alterValue(idf, classNameChild, variable, variableConfigChild, newValue)

    def alterValue(self, idf, className, variable, variableConfig, parentValue, identifier = None):
        newValue = self.getNewValueFromConfig(variableConfig['alg'], variableConfig['parameters'], parentValue)
        self.configString += ',' + newValue
        if (identifier == None):
            idf.getObjectByClass(className).setParameterByName(variable, newValue)
            self.header += ',' + className + ':' + variable
        else:
            idf.getObjectByClass(className, identifier).setParameterByName(variable, newValue)
            self.header += ',' + className + ':' + identifier + ':' + variable
        if ('change' in variableConfig):
            self.iterateOverClasses(idf, sorted(variableConfig['change'].items()), newValue)

    def createIdfs(self):
        progressbar.printProgressBar(0, self.config['quantity']+1, prefix = 'Progress:', suffix = 'Complete', length = 50)

        # gera a quatidade de idf's configurada
        for x in range(1,self.config['quantity']+1):

            filename = self.config['path']['filename'] + '' + str(x) + '.idf'
            self.header = 'output'
            self.configString = filename

            # instancia a classe do idf a partir do idf base
            idf = idfset.IDFSet(self.config['path']['base'])

            self.iterateOverClasses(idf, sorted(self.config['variables'].items()), 0)

            # gera os idf´s novos com as variações da configuração
            if (not self.wroteHeader):
                self.createParameterFile(self.header)
                self.wroteHeader = True
            self.createParameterFile(self.configString)

            idf.generateIdf(self.config['path']['destination'] + '/' + filename)

            progressbar.printProgressBar(x+1, self.config['quantity']+1, prefix = 'Progress:', suffix = 'Complete', length = 50)
