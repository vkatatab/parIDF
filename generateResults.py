import sys
import json
import os
import shutil
import glob
import ntpath
import csv
import collections
from subprocess import call
from tqdm import tqdm
import re

filename = 'files/resultConfig.json'
fp = open(filename)
file = fp.read()
config = json.loads(file)

globString = config['path']['destination'] + '/**/*.idf'
globFiles = sorted(glob.glob(globString), key=lambda name: int(re.findall('\d+|$', name)[0]))

results = config['results']

for resultName in tqdm(results):
    resultDict = collections.OrderedDict()
    resultConfig = results[resultName]
    for globFile in tqdm(globFiles):
        basename = ntpath.basename(globFile)
        splittedName = os.path.splitext(basename)
        if (resultConfig['meter']):
            filename = config['path']['source'] + '/' + splittedName[0] + 'Meter.csv'
        else:
            filename = config['path']['source'] + '/' + splittedName[0] + '.csv'
        with open(filename) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                for column in resultConfig['columns']:
                    newColumn = column + '<' + splittedName[0] + '>'
                    if (newColumn not in resultDict):
                        resultDict[newColumn] = []
                    resultDict[newColumn].append(row[column])

    columns = []
    for column in resultDict:
        columns.append(column)

    with open(config['path']['destination'] + '/' + resultName, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns)

        writer.writeheader()
        size = len(resultDict[columns[0]])
        for i in range(0, size):
            dictRow = collections.OrderedDict()
            for column in resultDict:
                dictRow[column] = resultDict[column][i].strip()
            writer.writerow(dictRow)

print ("*** The selected columns results of the all simulations have been united ***")
