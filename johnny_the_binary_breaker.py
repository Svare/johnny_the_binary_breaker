
#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import re
import os
from sys import argv

def get_files_names(dirs_paths, harcoded_exts, verbose):

    files_names = []

    for dir_path in dirs_paths:
        if verbose:                                                 # Verbose
            print("\nGetting files from folder: \n\n\t" + dir_path)   # Verbose
            print("\n\tFiles:\n")
        i = 0                                                       # Verbose
        for r, d, f in os.walk(dir_path): # root directory file
            for file_name in f:
                if file_name.endswith(tuple(harcoded_exts)):
                    files_names.append(os.path.join(r, file_name))
                    if verbose:                                     # Verbose
                        print("\t\t" + os.path.join(r, file_name))  # Verbose
                    i += 1                                          # Verbose
        if verbose:                                                 # Verbose
            print("\n\tFound " + str(i) + " files\n")                   # Verbose

    return files_names

def get_harcoded_data(files):

    regular_expressions = [
        re.compile(r'char\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\[\s*(?:\d*|(?:[a-zA-Z_][a-zA-Z0-9_]*))?\s*\]\s*=\s*".*"\s*;'), #char name[] = "";
        re.compile(r'char\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\[\s*(?:\d*|(?:[a-zA-Z_][a-zA-Z0-9_]*))?\s*\]\s*=\s*{.*}\s*;'), #char name[] = {};
        re.compile(r'char\s*\*\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*".*"\s*;'), #char*
        re.compile(r'int\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(?:\+|-)?\s*\d+\s*;'), #int
        re.compile(r'(?:float|double)\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*[-+]?[0-9]*[.]?[0-9]+([eE][-+]?[0-9]+)?\s*;'), #float, double
        #re.compile(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*".*";'), #Igualaciones char
        #re.compile(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(?:\+|-)?\s*\d+\s*;'),#Igualaciones int
        #re.compile(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*[-+]?[0-9]*[.]?[0-9]+([eE][-+]?[0-9]+)?\s*;'), #Igualaciones float, double
        #re.compile(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*= *[^\s;]+ *;') #Cualquier tipo de igualacion
    ]
    
    log = {}
    
    for file_abs_name in files:

        log[file_abs_name] = []

        with open(file_abs_name, 'r') as current_file:
            i = 1
            for line in current_file.readlines():
                for regex in regular_expressions:
                    result = re.search(regex, line)
                    #print(i, result, regex, line) #verbose
                    if result is not None:
                        log[file_abs_name].append((i, result.group()))
                        break
                i+=1
    
    print(log)

if __name__ == "__main__":

    with open(argv[1], 'r') as config_file:
        config = json.load(config_file)

    get_harcoded_data(get_files_names(config['dirs_paths'], config['harcoded_exts'], config['verbose']))