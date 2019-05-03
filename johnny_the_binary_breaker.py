#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import re
import os
import subprocess

from sys import argv
from functools import reduce

# Nuestros Modulos

import static_analysis
import functions_sweeper
import compile
import make_program
import recognition_phase
import compare_recognition
import destruction_phase

from get_segmentation_fault import get_breakpoint

if __name__ == "__main__":

    json_config = static_analysis.get_config_json_dict(argv[1]) # Se carga el archivo json de configuracion
    
    if json_config['hardcoded']:

        files_names = static_analysis.get_files_names(json_config)  # Se obtienen todos los nombres de los archivos

        # harcoded_data_dic: Diccionario con los valores harcodeados.
        # MAX_INT: El numero entero maximo encontrado en los archivos.
        # main_arg: nombre del arreglo que se le pasa al main
        
        # Se imprimen los valores harcodeados

        harcoded_data_dict, MAX_INT = static_analysis.get_harcoded_data(files_names, json_config)
        static_analysis.print_harcoded_data(harcoded_data_dict)
    
    # Obtencion de llamadas a funciones dentro de cada funcion con sus respectivos parametros
    
    with open(json_config['main_file'], 'r') as archivo:
            file_chars = archivo.read()

    l1 = functions_sweeper.get_functions_definitions(file_chars)
    d1 = functions_sweeper.get_functions_bodys(file_chars, functions_sweeper.get_functions(file_chars, l1))
    d2 = functions_sweeper.get_functions_calls_per_function(d1)
    
    buffer_overflow_func_catalog = functions_sweeper.get_buffer_overflow_funcs(d2)

    # Se buscan y se imprimen las funciones vulnerables, las criticas estan acompañandas de un comentario

    if json_config['vulnerable_funcs']:
        functions_sweeper.get_vulnerable_funcs(d2, static_analysis.get_argv(file_chars))

    # ##### Generacion del Binario (compile | make_program) #####

    # if json_config['gcc_main_path'] is not None:
    #     compile.compile_file(json_config['gcc_main_path'])
    # elif json_config['make_path'] is not None:
    #     make_program.do_make(json_config['make_path'])
    
    ##### recognition_phase #####

    if json_config['binary_path'] is not None:
        recognition_phase.run_recognition_phase(json_config['binary_path'], buffer_overflow_func_catalog)
        
        print('\nDiccionario Ensamblador\n')
        print(recognition_phase.asm_funct_call)
        print('\nDiccionario Fuente\n')
        print(buffer_overflow_func_catalog)
    
    ##### Comparacion #####

    if buffer_overflow_func_catalog and recognition_phase.asm_funct_call: # Si los diccionarios no estan vacios
        buffer_overflow_func_catalog, asm_funct_call = compare_recognition.compare_dicts(buffer_overflow_func_catalog, recognition_phase.asm_funct_call)
    
    ##### destruction_phase #####
    
    if json_config['binary_path'] is not None:
        lista_asquerosa = destruction_phase.destruction_phase(json_config['binary_path'], asm_funct_call)
        print(lista_asquerosa)


    #### explotation #####

    payload_length = get_breakpoint(info_list, binary_path) + 4 # Cuatro del Tamaño de la Direccion de Memoria