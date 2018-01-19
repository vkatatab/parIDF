import sys
import json
import os
import shutil
import glob
import ntpath
from subprocess import call
from joblib import Parallel, delayed
import multiprocessing

# sys.path.insert: possibilita a importação de classes em uma subpasta
sys.path.insert(0, 'classes')

import main

filename = 'files/config.json'
fp = open(filename)
file = fp.read()
config = json.loads(file)
idf = main.Main(filename)

idf.createIdfs()

def runEnergyPlus(outputName,weatherFilename):
	call(["runenergyplus", outputName, weatherFilename])


run = input ("*** Do you want to simulate all the created IDF's files? (Y/n):\n")
# # Y representa Yes e será o default e n representa No
if run.lower() == "y" or run.lower() == "":
    energyplusOutput = config['path']['destination'] + '/Output'
    if (os.path.isdir(energyplusOutput)):
        shutil.rmtree(energyplusOutput)
    globName = config['path']['destination'] + '/' + config['path']['filename'] + '*.idf'
    weatherFilename = config['path']['weatherFilename']
    globFiles = glob.glob(globName)
    num_cores = multiprocessing.cpu_count()
    Parallel(n_jobs=num_cores)(delayed(runEnergyPlus)(outputName, weatherFilename) for outputName in globFiles)
    print ("*** The IDF files simulations have been successfully completed ***")

# energyplus -i custom.idd -w weather.epw input.idf
# Example: energyplus -w weather.epw -r input.idf
#-x, --expandobjects Run ExpandObjects prior to simulation

    for extension in ['err', 'csv']:
        extensionFolder = energyplusOutput + '/' + extension
        if not os.path.exists(extensionFolder):
            os.makedirs(extensionFolder)
        globName = energyplusOutput + '/' + config['path']['filename'] + '*.' + extension
        for file in glob.glob(globName):
            os.rename(file, extensionFolder + '/' + ntpath.basename(file))

if run.lower () == "n":
     print ("*** The IDF files haven't been executed by EnergyPlus, but they are saved in the destination folder ***")
