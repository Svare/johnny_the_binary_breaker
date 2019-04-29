
import json
import re
import os

from sys import argv
from functools import reduce

def get_config_json_dict(json_config_file):

    with open(argv[1], 'r') as config_file:
        return json.load(config_file)

def get_files_names(json_config):

    files_names = []

    for dir_path in json_config['dirs_paths']:
        if json_config['verbose']:                                          # Verbose
            print("\nGetting files from folder: \n\n\t" + dir_path)         # Verbose
            print("\n\tFiles:\n")                                           # Verbose
        i = 0                                                               # Verbose
        for r, d, f in os.walk(dir_path): # root directory file
            for file_name in f:
                if file_name.endswith(tuple(json_config['harcoded_exts'])):
                    files_names.append(os.path.join(r, file_name))
                    if json_config['verbose']:                              # Verbose
                        print("\t\t" + os.path.join(r, file_name))          # Verbose
                    i += 1                                                  # Verbose
        if json_config['verbose']:                                          # Verbose
            print("\n\tFound " + str(i) + " files\n")                       # Verbose

    return files_names

def get_harcoded_data(files, json_config):

    MAX_INT = 0
    main_arg = 'Not Found'

    regular_expressions = [
        re.compile(r'char\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\[\s*(?:\d*|(?:[a-zA-Z_][a-zA-Z0-9_]*))?\s*\]\s*=\s*".*"\s*;'), #char name[] = "";
        re.compile(r'char\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*ñ\s*=\s*{.*}\s*;'), #char name[] = {};
        re.compile(r'char\s*\*\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*".*"\s*;'), #char*
        re.compile(r'int\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(?:\+|-)?\s*\d+\s*;'), #int
        #re.compile(r'(?:float|double)\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*[-+]?[0-9]*[.]?[0-9]+([eE][-+]?[0-9]+)?\s*;'), #float, double
        #re.compile(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*".*";'), #Igualaciones char
        #re.compile(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(?:\+|-)?\s*\d+\s*;'),#Igualaciones int
        #re.compile(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*[-+]?[0-9]*[.]?[0-9]+([eE][-+]?[0-9]+)?\s*;'), #Igualaciones float, double
        #re.compile(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*= *[^\s;]+ *;') #Cualquier tipo de igualacion
    ]

    integers = [
        re.compile(r'#define\s+(?:[a-zA-Z_][a-zA-Z0-9_]*)\s+([0-9]+)\s*'),
        re.compile(r'(?:[a-zA-Z_][a-zA-Z0-9_]*)\s*\=\s*([0-9]+)\s*[,;]')
    ]

    # main = re.compile('main\s*\(\s*.*char\s*(?:\*\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\[\s*\]|\*\s*\*\s*([a-zA-Z_][a-zA-Z0-9_]*))[^)]*\)')
    
    log = {}
    
    for file_abs_name in files:

        log[file_abs_name] = []

        with open(file_abs_name, 'r') as current_file:
            i = 1
            for line in current_file.readlines():

                for regex in regular_expressions:
                    result = re.search(regex, line)
                    if result is not None:
                        log[file_abs_name].append((i, result.group()))
                        break
                
                # Obtencion del valor entero maximo.

                for regex in integers:

                    while '"' in line:
                        line = line[:line.index('"')] + line[line.index('"', int(line.index('"') + 1)) + 1 :]

                    result = re.findall(regex, line)

                    if result:
                        for value in result:
                            #print(value) # Verbose
                            MAX_INT = int(value) if (int(value) > MAX_INT) else MAX_INT
                        break
                
                # # Obtencion del nombre de los argumentos pasados por linea de comandos 
                
                # result = re.search(main, line)

                # if result is not None:
                #     main_arg = result.groups()[0] if (result.groups()[0] is not None) else result.groups()[1]

                i+=1
    
    return log, MAX_INT

def get_main_arg(file_chars):

    # Obtencion del nombre de los argumentos pasados por linea de comandos

    main = re.compile('main\s*\(\s*.*char\s*(?:\*\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\[\s*\]|\*\s*\*\s*([a-zA-Z_][a-zA-Z0-9_]*))[^)]*\)')
    result = re.search(main, file_chars)

    if result is not None:
        main_arg = result.groups()[0] if (result.groups()[0] is not None) else result.groups()[1]
    else:
        main_arg = 'argv'
    
    return main_arg

def print_harcoded_data(log):

    for key, value in log.items():
        print('\n' + key + '\n')
        for harcoded_item in value:
            print('\t{0:>8}\t{1}'.format(str(harcoded_item[0]), harcoded_item[1]))
    print()