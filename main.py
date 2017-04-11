import sys

sys.path.insert(0, 'classes')

import re
import idfobject
import idfset
import json

fp = open('config.json')
file = fp.read()
config = json.loads(file)

for x in xrange(1,config['quantity']+1):
    idf = idfset.IDFSet(config['path']['base'])
    for (className, classConfig) in config['variables'].items():
        if ('identifiers' in classConfig):
            for (identifier, identifierConfig) in classConfig['identifiers'].items():
                for (variable, variableConfig) in identifierConfig.items():

                    algName = variableConfig['alg']
                    module = __import__(algName.lower())
                    class_ = getattr(module, algName)
                    instance = class_(variableConfig['parameters'])

                    idf.getObjectByClass(className, identifier).setParameterByName(variable, instance.getNewValue())
        else:
            for (variable, variableConfig) in classConfig.items():

                algName = variableConfig['alg']
                module = __import__(algName.lower())
                class_ = getattr(module, algName)
                instance = class_(variableConfig['parameters'])

                idf.getObjectByClass(className).setParameterByName(variable, instance.getNewValue())
    idf.generateIdf( config['path']['destination'] + '/' + config['path']['filename'] + '' + str(x) + '.idf')