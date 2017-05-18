import sys
import json

# sys.path.insert: possibilita a importação de classes em uma subpasta
sys.path.insert(0, 'classes')

import main

# idf = main.Main('files/config.json')

# idf.createIdfs()

run = input ("Do you want to simulate all the created IDF's files? (Y/n):\n")
# Y representa Yes e será o default e n representa No
if run.lower() == "y" or run.lower() == "":
    print ("executando")


if run.lower () == "n":
     print ("não executado")
