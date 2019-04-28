
import re
from sys import argv
from functools import reduce

def get_functions(full_file, possible_matches):

    matches = []
    words_blacklist = ['if', 'for', 'switch', 'do', 'while']
    operators = ['=', '==', '!=', '||', '&&', '<', '>', '<=', '>=']

    name = re.compile('([a-zA-Z_][a-zA-Z0-9_]*)\s*\(')

    for match in possible_matches:

        func_sign = full_file[full_file.find(match):full_file.find('{', full_file.find(match))]

        # Si la firma de la funcion tiene cualquiera de los operadores

        if reduce(lambda x,y: x or y, map(lambda operator: operator in func_sign, operators)):
            continue
                
        func_name = re.findall(name, func_sign)

        # Si el nombre de la funcion es igual a cualquiera de los que se encuentran en words_blacklist

        if reduce(lambda x, y: x or y, map(lambda word: word == func_name[0], words_blacklist)):
            continue
        
        matches.append((func_name[0], match))
    
    return matches

def get_functions_calls(full_file):

    stack = []
    global_index = 0
    func_calls_list = []

    func_call = re.compile(r'(?:[a-zA-Z_][a-zA-Z0-9_]*)\s*\(')

    func_calls = re.findall(func_call, full_file)
    string = full_file

    for match in func_calls:

        global_index = string.find(match)   # Valor inicial principio de la primera llamada a funcion
        global_index += len(match)          # Se posiciona en el caracter despues de (
        i = global_index
        buffer = ''
        stack.append('(')

        while True:

            if string[i] == '(':
                stack.append('(')
            elif string[i] == ')':
                stack.pop()
            
            buffer+=string[i]
            i+=1

            if len(stack) == 0:
                args = buffer
                break
        
        string = string[global_index:]

        if '(' in buffer[:-1]:
            args = [buffer[:-1]]
        else:
            args = list(map(lambda x: x.strip(), buffer[:-1].split(',')))
        
        func_calls_list.append((match.split('(')[0].strip(), args))
    
    return func_calls_list

def get_functions_bodys(full_file, matches):

    functions_bodys_dict = {}
    stack = []

    for j in range(len(matches)):

        func_name = matches[j][0]
        match = matches[j][1]
        buffer = ''
        i = full_file.find('{', full_file.find(match))

        while True:

            try:

                if full_file[i] == '{':
                    stack.append('{')
                elif full_file[i] == '}':
                    stack.pop()
                
                buffer += full_file[i]
                i += 1

                if len(stack) == 0:
                    functions_bodys_dict[func_name] = buffer
                    break
    
            except IndexError:
                
                stack = []

                if j+1 < len(matches):
                    tmp = full_file.find(matches[j+1][1])
                    indx = full_file[:tmp].rfind('}')
                    functions_bodys_dict[func_name] = full_file[full_file.find('{', full_file.find(match)):indx] + '}'
                else:
                    functions_bodys_dict[func_name] = full_file[full_file.find('{', full_file.find(match)):]

                break
            
    
    return functions_bodys_dict

def get_functions_calls_per_function(functions_bodys_dict):

    functions_calls_per_function = {}

    for func, body in functions_bodys_dict.items():
        functions_calls_per_function[func] = get_functions_calls(body)
    
    return functions_calls_per_function

def get_buffer_overflow_funcs(functions_calls_per_function):

    buffer_overflow_candidates = {}
    temp_funcs = []

    vulnerable = ('scanf', 'gets', 'strcpy', 'strncpy')

    for func, calls_list in functions_calls_per_function.items():
        for name, args in calls_list:
            if name.startswith(vulnerable) and name.endswith(vulnerable):
                temp_funcs.append(name)
        buffer_overflow_candidates[func] = temp_funcs
        temp_funcs = []
    
    return buffer_overflow_candidates

if __name__ == "__main__":

   # r = re.compile('(?:(?:[a-zA-Z_][a-zA-Z0-9_]*) +)+(?:[a-zA-Z_][a-zA-Z0-9_]*)\s*\([^(]*\)\s*{')

    r = re.compile('(?:(?:[a-zA-Z_][a-zA-Z0-9_]*) +)+\s*\*?\s*(?:[a-zA-Z_][a-zA-Z0-9_]*)\s*\([^(]*\)\s*{')
    
    with open(argv[1], 'r') as archivo:
        
        # Full File

        read_file = archivo.read()
        result = re.findall(r, read_file)

      #  print(result)
    
    s = get_functions_bodys(read_file, get_functions(read_file, result))
    w = get_functions_calls_per_function(s)
    
    print(get_buffer_overflow_funcs(w))
   
   