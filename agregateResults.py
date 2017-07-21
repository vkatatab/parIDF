import sys
import json
import os
import shutil
import glob
import ntpath
import csv
import re
from subprocess import call

filename = 'files/agregateConfig.json'
fp = open(filename)
file = fp.read()
config = json.loads(file)

source = config['path']['source'] + '/'

files = config['files']

for filename in files:
    fullPath = source + filename

    with open(fullPath, "r") as f:
        reader = csv.reader(f)
        columns = next(reader)
    outputs = []
    for columnName in columns:
        result = re.findall('.*\<(.*)\>', columnName)
        outputs.append(result[0])
    outputs = set(outputs)

    newHeader = ['file']
    newRows = []
    newDict = {}

    for column in config['files'][filename]['columns']:
        formulas = config['files'][filename]['columns'][column]['values']
        for formula in formulas:
            header = column + '<' + formula + '>'
            if (header not in newHeader):
                newHeader.append(header)

    for column in config['files'][filename]['columns']:
        formulas = config['files'][filename]['columns'][column]['values']
        for output in outputs:
            SUM = 0
            COUNT = 0
            AVG = 0
            MAX = -float("inf")
            MIN = float("inf")
            newDict['file'] = output
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
                        newDict[header] = eval(formula)

                if (len(newHeader) == len(newDict)):
                    newRows.append(newDict.copy())
                    newDict = {}
        print(newRows)

    with open(config['path']['destination'] + '/aaaa.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=newHeader)

        writer.writeheader()
        for row in newRows:
            writer.writerow(row)

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
