# -*- coding: utf-8 -*-
# Esse arquivo modela e ordena as classes com os respectivos parâmetros do IDF
# Além disso é reponsável por escrever um novo IDF
# A organização é realizada:
#   - De acordo com a organizacão recebida pelo IDF base
#   - Identifica-se e agrupa-se objetos de uma mesma classe

# imports : importa as classes necessárias
import re
import collections
# importa a classe de objetos IDF
import idfobject

# Classe no sistema que represta um conjunto de classes do IDF
class IDFSet(object):
    # O construtor da classe recebe por parametro o caminho do arquivo IDF base
    def __init__(self, path):
        self.path = path
        self.set = collections.OrderedDict()
        self.parseFile()

    # Analisa o arquivo encontrado no caminho definido e guarda um conjunto de objetos referentes a cada classe do IDF
    def parseFile(self):
        fp = open(self.path)
        file = fp.read()
        objectStrings = re.findall('((.+),[\n\r]+((.+)[,;]\s*!-.+[\n\r])+)', file)
        # Percorre todas as classes do IDF
        for objectString in objectStrings:
            tempObject = idfobject.IDFObject(objectString[0])
            tempObjectClass = tempObject.getIdfClass()

            # Caso a classe seja de output
            if (tempObjectClass == 'Output:Variable'):
                if (tempObjectClass not in self.set):
                    self.set[tempObjectClass] = []
                self.set[tempObjectClass].append(tempObject)

            # Caso a classe já esteja no conjunto
            elif (tempObjectClass in self.set):
                conflictClass = self.set[tempObjectClass]

                # Se temos apenas um objeto em uma classe
                if (len(conflictClass) == 1):
                    # Adicionamos a possibilidade de termos mais de um e adicionamos o novo objeto
                    identifierName = conflictClass.getIdentifier().strip()
                    identifierValue = conflictClass.getParameterByName(identifierName)
                    self.set[tempObjectClass] = {}
                    self.set[tempObjectClass][identifierValue] = conflictClass

                identifierName = tempObject.getIdentifier().strip()
                identifierValue = tempObject.getParameterByName(identifierName)
                self.set[tempObjectClass][identifierValue] = tempObject

            # Caso não seja nenhuma das opções apenas adicionamos
            else:
                self.set[tempObjectClass] = tempObject

    # Retorna uma única classe do IDF a partir do nome e se necessário um identificador
    # Caso não seja encontrar é retornado None
    def getObjectByClass(self, className, identifierName = None):
        if (className in self.set):
            if (len(self.set[className]) > 1):
                if (identifierName == None):
                    return None
                elif (identifierName in self.set[className]):
                    return self.set[className][identifierName]
                else:
                    return None
                print('className')
            else:
                return self.set[className]
        else:
            return None

    # Método responsável por gerar o IDF
    def generateIdf(self, path):
        fp = open(path, 'w')
        for (className, idfobject) in self.set.items():
            if (className == 'Output:Variable'):
                for idfobjectChild in idfobject:
                    fp.write(idfobjectChild.getObjectString())
                    fp.write('\n\r')
            elif (len(idfobject) > 1):
                for (className, idfobjectChildren) in idfobject.items():
                    # print (idfobjectChildren)
                    fp.write(idfobjectChildren.getObjectString())
                    fp.write('\n\r')
            else:
                fp.write(idfobject.getObjectString())
                fp.write('\n\r')
