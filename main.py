import sys
import re

sys.path.insert(0, 'classes')

import idfobject

aux = []
fp = open('files/base.idf')
file = fp.read()

idfobjects = {}

objects = re.findall('((.+),[\n\r]+((.+)[,;]\s*!-.+[\n\r])+)', file)
i = 0
for objeto in objects:
    aux = idfobject.IDFObject(objeto[0])
    idfobjects[aux.getIdfClass()] = aux

idfobjects['ElectricEquipment'].setParameterByClass('Watts per Zone Floor Area {W/m2}', 20)
print(idfobjects['ElectricEquipment'].getParameterByClass('Watts per Zone Floor Area {W/m2}'))


# teste = idfobject.IDFObject(""" SimulationControl,
#     No,                      !- Do Zone Sizing Calculation
#     ,                      !- Do System Sizing Calculation
#     No,                      !- Do Plant Sizing Calculation
#     No,                      !- Run Simulation for Sizing Periods
#     Yes;                     !- Run Simulation for Weather File Run Periods """)

# print(teste.getParameterByName('Do System Sizing Calculation'))