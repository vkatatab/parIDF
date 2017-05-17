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

# inicia a leitura do arquivo de configuração
fp = open('config.json')
file = fp.read()
config = json.loads(file)
# finaliza a leitura do arquivo de configuração


# gera a quatidade de idf's configurada
for x in range(1,config['quantity']+1):

    # instancia a classe do idf a partir do idf base
    idf = idfset.IDFSet(config['path']['base'])

    # itera sobre todas as variáveis configuradas para serem alteradas
    for (className, classConfig) in config['variables'].items():

        #verifica se a classe não é única, que tem mais de um objeto do idf em uma mesma classe
        if ('identifiers' in classConfig):

            # itera sobre todos os objetos do idf de uma mesma classe
            for (identifier, identifierConfig) in classConfig['identifiers'].items():

                #percorre a configuração preparando para realizar a troca dos valores
                for (variable, variableConfig) in identifierConfig.items():

                    algName = variableConfig['alg']
                    module = __import__(algName.lower())
                    class_ = getattr(module, algName)
                    instance = class_(variableConfig['parameters'])

                    idf.getObjectByClass(className, identifier).setParameterByName(variable, instance.getNewValue())

        #caso a clase seja única
        else:

            for (variable, variableConfig) in classConfig.items():

                algName = variableConfig['alg']
                module = __import__(algName.lower())
                class_ = getattr(module, algName)
                instance = class_(variableConfig['parameters'])

                idf.getObjectByClass(className).setParameterByName(variable, instance.getNewValue())

    # gera os idf´s novos com as variações da configuração
    idf.generateIdf( config['path']['destination'] + '/' + config['path']['filename'] + '' + str(x) + '.idf')
