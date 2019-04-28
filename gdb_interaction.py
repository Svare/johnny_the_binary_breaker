#!/usr/bin/python3
from pwn import *

asm_funct_call = {}
time_out = 0.2

#ejecuta gdb
def exec_gdb(file_name):
    return process(['/usr/bin/gdb', file_name , '-q'])

#imprime con utf-8 las lineas adquiridas desde recvlines
def print_stdout(lines):
    for line in lines:
        print(line.decode('utf-8'))

#identifica si la linea asm tiene un call
def idenfi_call_lines(line):
    if 'call' in line:
        return True
    return False

#
def

#mapea las funciones con los opcodes call
def map_functions(gdb , funtions_dict):
    for fun in funtions_dict.keys():
        gdb.sendline('disass {}'.format(fun))
        lines = gdb.recvlines(timeout=time_out)
        for line in lines:


#funcion general que realiza la fase de reconocimiento
def run_recognition_phase(executable, funtions_dict):
        gdb = exec_gdb(executable)
        gdb.recvlines(timeout=time_out)
        #print_stdout(gdb.recvlines(timeout=0.2))

        gdb.sendline('b main')
        gdb.recvlines(timeout=time_out)
        #print_stdout(gdb.recvlines(timeout=0.2))

        gdb.sendline('run')
        gdb.recvlines(timeout=time_out)
        #print_stdout(gdb.recvlines(timeout=0.2))

        map_functions(gdb, funtions_dict)


        gdb.close()

        run_recognition_phase('../x.out', d)
if __name__ == '__main__':
    d = {'r':[], 'main':[]}
