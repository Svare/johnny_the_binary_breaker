#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import re
import os

from sys import argv
from functools import reduce

# Nuestros Modulos

import static_analysis
import functions_sweeper
import compile
import make_program
import recognition_phase
import compare_recognition

if __name__ == "__main__":

    json_config = static_analysis.get_config_json_dict(argv[1]) # Se carga el archivo json de configuracion
    files_names = static_analysis.get_files_names(json_config)  # Se obtienen todos los nombres de los archivos

    # harcoded_data_dic: Diccionario con los valores harcodeados.
    # MAX_INT: El numero entero maximo encontrado en los archivos.
    # main_arg: nombre del arreglo que se le pasa al main

    harcoded_data_dict, MAX_INT, main_arg = static_analysis.get_harcoded_data(files_names, json_config) # Se buscan valores harcodedados
    
    # Se imprimen los valores harcodeados

    if json_config['hardcoded']:
        static_analysis.print_harcoded_data(harcoded_data_dict)
    
    # Obtencion de llamadas a funciones dentro de cada funcion con sus respectivos parametros
    
    with open(json_config['main_file'], 'r') as archivo:
            file_chars = archivo.read()

    l1 = functions_sweeper.get_functions_definitions(file_chars)
    d1 = functions_sweeper.get_functions_bodys(file_chars, functions_sweeper.get_functions(file_chars, l1))
    d2 = functions_sweeper.get_functions_calls_per_function(d1)
    
    buffer_overflow_func_catalog = functions_sweeper.get_buffer_overflow_funcs(d2)

    ##### Generacion del Binario (compile | make_program) #####

    if json_config['gcc_main_path'] is not None:
        compile.compile_file(json_config['gcc_main_path'])
    elif json_config['make_path'] is not None:
        make_program.do_make(json_config['make_path'])
    
    ##### recognition_phase #####

    if json_config['binary_path'] is not None:
        recognition_phase.run_recognition_phase(json_config['binary_path'], buffer_overflow_func_catalog)
        print(recognition_phase.asm_funct_call)
    
    ##### Comparacion #####

    if buffer_overflow_func_catalog and recognition_phase.asm_funct_call: # Si los diccionarios no estan vacios
        print(compare_recognition.compare_dicts(buffer_overflow_func_catalog, recognition_phase.asm_funct_call))

    #print(MAX_INT, main_arg)