
import re
from sys import argv
from functools import reduce

def get_functions_definitions(file_chars):

    ''' Regresa una lista con las firmas de todas las funciones que encuentra en el archivo file_chars. '''

    functions_definitions = re.compile('(?:(?:[a-zA-Z_][a-zA-Z0-9_]*) +)+\s*\*?\s*(?:[a-zA-Z_][a-zA-Z0-9_]*)\s*\([^(]*\)\s*{')
    
    return re.findall(functions_definitions, file_chars)

def get_functions(full_file, possible_matches):

    ''' Regresa una lista de tuplas de 2 elementos, el primer elemento es el nombre de la funcion y el segundo elemento
        es la firma de dicha funcion. '''

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

def get_functions_bodys(full_file, matches):

    ''' Regresa un diccionario donde las llaves son los nombres de las funciones y los valores son todo el cuerpo de
        las funciones, es decir lo que estas encierran dentro de las llaves {}. '''

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

def get_functions_calls(full_file):

    ''' Regresa una lista de tuplas donde el primer elemento de cada tupla es el nombre de la funcion que se esta
        llamando dentro de otras funciones y el segundo elemento es una lista con los argumentos que se le estan
        pasando a la funcion.
        
        Bugs:
        
            Esta funcion detecta a los ciclos como for, while, switch como funciones por lo que son falsos positivos
            que deben de ser ignorados, para esto se debe de volver a parsear la lista. '''

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

def get_functions_calls_per_function(functions_bodys_dict):

    ''' Obtiene todas las llamadas a funciones dentro de cada funcion del diccionario que se le pasa (functions_bodys_dict)
        para esto aplica get_functions_calls a cada uno de los cuerpos dentro del diccionario.
        
        Regresa un diccionario donde las llaves son los nombres de las funciones y el valor es una lista de tuplas donde cada
        tupla esta formada por dos elementos el primer elemento de la tupla es el nombre de la funcion que esta siendo llamada,
        y el segundo elemento es una lista que contiene los parametros/argumentos de la funcion que esta siendo llamada. '''

    functions_calls_per_function = {}

    for func, body in functions_bodys_dict.items():
        functions_calls_per_function[func] = get_functions_calls(body)
    
    return functions_calls_per_function

def get_buffer_overflow_funcs(functions_calls_per_function):

    ''' Obtiene las llamadas a funciones vulnerables a buffer overflow dentro de cada funcion.
    
        Regresa un diccionario donde cada llave es el nombre de la funcion y el valor es una lista de cadenas
        donde cada cadena es el nombre de una funcion vulnerable a buffer overflow. '''

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

def get_vulnerable_funcs(functions_calls_per_function, main_arg):

    report = ''
    vulnerable = ('scanf', 'gets', 'strcpy', 'strncpy', 'printf')
    var_name = re.compile(r'([a-zA-Z_][a-zA-Z0-9_]*)')

    for func, calls_list in functions_calls_per_function.items():

        print('Funcion: ' + func)
        print('\n\t\tLlamadas Vulnerables: \n')
        report += 'Funcion' + func + '\n\t\tFunciones Vulnerables: '
        
        for name, args in calls_list:
            if name.startswith(vulnerable) and name.endswith(vulnerable):
                print('\t\t\t', name, args)
                if name == 'strcpy':
                    if len(args) == 2 and main_arg in args[1]:
                        print('\n\t\t\t\t*********************************')
                        print('\t\t\t\t*** This is Very Risky Dog ******')
                        print('\t\t\t\t*********************************')
                        print('\t\t\t\t*** Potential Buffer Overflow ***')
                        print('\t\t\t\t*********************************\n')
                elif name == 'gets':
                    if len(args) == 1 and re.match(var_name, args[0]) is not None:
                        print('\n\t\t\t\t*********************************')
                        print('\t\t\t\t*** This is Very Risky Dog ******')
                        print('\t\t\t\t*********************************')
                        print('\t\t\t\t*** Potential Buffer Overflow ***')
                        print('\t\t\t\t*********************************\n')
                elif name == 'printf':
                    if len(args) == 1 and re.match(var_name, args[0]) is not None:
                        print('\n\t\t\t\t*********************************')
                        print('\t\t\t\t*** This is Very Risky Dog ******')
                        print('\t\t\t\t*********************************')
                        print('\t\t\t\t*** Potential Format String *****')
                        print('\t\t\t\t*********************************\n')
        print()

if __name__ == "__main__":

    with open(argv[1], 'r') as archivo:
        file_chars = archivo.read()
    
    l1 = get_functions_definitions(file_chars)
    d1 = get_functions_bodys(file_chars, get_functions(file_chars, l1))
    d2 = get_functions_calls_per_function(d1)
    print(get_buffer_overflow_funcs(d2))
   
   