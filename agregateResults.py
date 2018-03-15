# Esse é um código em script para a criação de uma planilha .csv que agrega resultados desejados
# da planilha .csv denominada generateResults.ṕy, através de relações e formulas fornecidas
# pelo usuário (exemplo: somatória da coluna, ver o valor minimo e etc) importando um arquivo json

import sys
import json
import os
import shutil
import glob
import ntpath
import csv
import re
import collections
from subprocess import call
from tqdm import tqdm

# inicia a leitura do arquivo de configuração
filename = 'files/agregateConfig.json'
fp = open(filename)
file = fp.read()
config = json.loads(file)

source = config['path']['source'] + '/'

files = config['files']

for filename in tqdm(files):
    fullPath = source + filename

    with open(fullPath, "r") as f:
        reader = csv.reader(f)
        columns = next(reader)
    outputs = []
    for columnName in columns:
        result = re.findall('.*\<(.*)\>', columnName)
        outputs.append(result[0])
    outputs = sorted(set(outputs))

    newHeader = ['file']
    newDict = collections.OrderedDict()

    for column in config['files'][filename]['columns']:
        formulas = config['files'][filename]['columns'][column]['values']
        for formula in formulas:
            header = column + '<' + formula + '>'
            if (header not in newHeader):
                newHeader.append(header)

    for column in config['files'][filename]['columns']:
        formulas = config['files'][filename]['columns'][column]['values']
        for output in outputs:
            if (output not in newDict):
                newDict[output] = collections.OrderedDict()
            SUM = 0
            COUNT = 0
            AVG = 0
            MAX = -float("inf")
            MIN = float("inf")
            newDict[output]['file'] = output
            with open(fullPath) as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    value = float(row[column + '<' + output + '>'])
                    SUM = SUM + value
                    COUNT = COUNT + 1
                    if (value >= MAX):
                        MAX = value
                    if (value <= MIN):
                        MIN = value
                    AVG = SUM/COUNT
                    for formula in formulas:
                        header = column + '<' + formula + '>'
                        newDict[output][header] = eval(formula)

    with open(config['path']['destination'] + '/agregate_' + filename, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=newHeader)

        writer.writeheader()
        for (name, parameter) in newDict.items():
            writer.writerow(parameter)

print ("*** The columns calculations results of the files have been created ***")

    # resultDict = {}
    # resultConfig = results[resultName]
    # for globFile in globFiles:
    #     basename = ntpath.basename(globFile)
    #     splittedName = os.path.splitext(basename)
    #     if (resultConfig['meter']):
    #         filename = config['path']['source'] + '/' + splittedName[0] + 'Meter.csv'
    #     else:
    #         filename = config['path']['source'] + '/' + splittedName[0] + '.csv'
    #     # print(filename)
    #
    # columns = []
    # for column in resultDict:
    #     columns.append(column)
    #
    # with open(config['path']['destination'] + '/' + resultName, 'w') as csvfile:
    #     writer = csv.DictWriter(csvfile, fieldnames=columns)
    #
    #     writer.writeheader()
    #     size = len(resultDict[columns[0]])
    #     for i in range(0, size):
    #         dictRow = {}
    #         for column in resultDict:
    #             dictRow[column] = resultDict[column][i].strip()
    #         writer.writerow(dictRow)
