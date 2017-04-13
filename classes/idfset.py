import re
import collections

import idfobject

class IDFSet(object):
    # O construtor da classe recebe por parametro o caminho do arquivo IDF base
    def __init__(self, path):
        self.path = path
        self.set = collections.OrderedDict()
        self.parseFile()

    def parseFile(self):
        fp = open(self.path)
        file = fp.read()
        objectStrings = re.findall('((.+),[\n\r]+((.+)[,;]\s*!-.+[\n\r])+)', file)
        for objectString in objectStrings:
            tempObject = idfobject.IDFObject(objectString[0])
            tempObjectClass = tempObject.getIdfClass()

            if (tempObjectClass == 'Output:Variable'):
                if (tempObjectClass not in self.set):
                    self.set[tempObjectClass] = []
                self.set[tempObjectClass].append(tempObject)

            elif (tempObjectClass in self.set):
                conflictClass = self.set[tempObjectClass]

                if (len(conflictClass) == 1):
                    identifierName = conflictClass.getIdentifier().strip()
                    identifierValue = conflictClass.getParameterByName(identifierName)
                    self.set[tempObjectClass] = {}
                    self.set[tempObjectClass][identifierValue] = conflictClass

                identifierName = tempObject.getIdentifier().strip()
                identifierValue = tempObject.getParameterByName(identifierName)
                self.set[tempObjectClass][identifierValue] = tempObject

            else:
                self.set[tempObjectClass] = tempObject

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

    def generateIdf(self, path):
        fp = open(path, 'w')
        for (className, idfobject) in self.set.items():
            if (className == 'Output:Variable'):
                for idfobjectChild in idfobject:
                    fp.write(idfobjectChild.getObjectString())
                    fp.write('\n');
            elif (len(idfobject) > 1):
                for (className, idfobjectChildren) in idfobject.items():
                    # print (idfobjectChildren)
                    fp.write(idfobjectChildren.getObjectString())
                    fp.write('\n\r');
            else:
                fp.write(idfobject.getObjectString())
                fp.write('\n\r');

    def printSet(self):
        print (self.set)