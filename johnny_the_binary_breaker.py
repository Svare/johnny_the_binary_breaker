
#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import re
import os
from sys import argv

def get_files_names(dirs_paths, harcoded_exts):

    files_names = []

    for dir_path in dirs_paths:
        for r, d, f in os.walk(dir_path): # root directory file
            for file_name in f:
                if file_name.endswith(tuple(harcoded_exts)):
                    files_names.append(os.path.join(r, file_name))
    #print(files_names) # Verbose
    return files_names

def get_harcoded_data(files):

    regular_expressions = [
        re.compile(r'char\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\[\s*?(?:\d*)\s*\]\s*=\s*".*"\s*;'),
        re.compile(r'char\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\[\s*?(?:\d*)\s*\]\s*=\s*{.*}\s*;'),
        re.compile(r'char\s*\*\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*".*"\s*;')
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
                        continue
                i+=1
    
    print(log)

if __name__ == "__main__":

    with open(argv[1], 'r') as config_file:
        config = json.load(config_file)

    get_harcoded_data(get_files_names(config['dirs_paths'], config['harcoded_exts']))
    
    


