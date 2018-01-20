import sys
import json
import os
import shutil
import glob
import ntpath
from subprocess import call
import subprocess
from joblib import Parallel, delayed
import multiprocessing
from tqdm import tqdm

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
	call(["runenergyplus", outputName, weatherFilename], stdout=subprocess.PIPE)

def text_progessbar(seq, total=None):
    step = 1
    tick = time.time()
    while True:
        time_diff = time.time()-tick
        avg_speed = time_diff/step
        total_str = 'of %n' % total if total else ''
        print('step', step, '%.2f' % time_diff,
              'avg: %.2f iter/sec' % avg_speed, total_str)
        step += 1
        yield next(seq)

all_bar_funcs = {
    'tqdm': lambda args: lambda x: tqdm(x, **args),
    'txt': lambda args: lambda x: text_progessbar(x, **args),
    'False': lambda args: iter,
    'None': lambda args: iter,
}

def ParallelExecutor(use_bar='tqdm', **joblib_args):
    def aprun(bar=use_bar, **tq_args):
        def tmp(op_iter):
            if str(bar) in all_bar_funcs.keys():
                bar_func = all_bar_funcs[str(bar)](tq_args)
            else:
                raise ValueError("Value %s not supported as bar type"%bar)
            return Parallel(**joblib_args)(bar_func(op_iter))
        return tmp
    return aprun


run = input ("*** Do you want to simulate all the created IDF's files? (Y/n):\n")
# # Y representa Yes e será o default e n representa No
if run.lower() == "y" or run.lower() == "":
    energyplusOutput = config['path']['destination'] + '/Output'
    if (os.path.isdir(energyplusOutput)):
        shutil.rmtree(energyplusOutput)
    globName = config['path']['destination'] + '/' + config['path']['filename'] + '*/' + config['path']['filename'] + '*.idf'
    weatherFilename = config['path']['weatherFilename']
    globFiles = glob.glob(globName)
    num_cores = multiprocessing.cpu_count()
    aprun = ParallelExecutor(n_jobs=num_cores)
    aprun(total=len(globFiles))(delayed(runEnergyPlus)(outputName, weatherFilename) for outputName in globFiles)
    print ("*** The IDF files simulations have been successfully completed ***")

# energyplus -i custom.idd -w weather.epw input.idf
# Example: energyplus -w weather.epw -r input.idf
#-x, --expandobjects Run ExpandObjects prior to simulation

    for extension in ['err', 'csv']:
        extensionFolder = energyplusOutput + '/' + extension
        if not os.path.exists(extensionFolder):
            os.makedirs(extensionFolder)
        globName = config['path']['destination'] + '/' + config['path']['filename'] + '*' + '/Output/' + config['path']['filename'] + '*.' + extension
        for file in glob.glob(globName):
            os.rename(file, extensionFolder + '/' + ntpath.basename(file))

if run.lower () == "n":
     print ("*** The IDF files haven't been executed by EnergyPlus, but they are saved in the destination folder ***")
