#!/usr/bin/python3
from pwn import *

functs_vulns =['gets','strcpy','scanf','strncpy']
asm_funct_call = {}
time_out = 0.1

#ejecuta gdb
def exec_gdb(file_name):
    return process(['/usr/bin/gdb', file_name , '-q'])

#imprime con utf-8 las lineas adquiridas desde recvlines
def print_stdout(lines):
    for line in lines:
        print(line.decode('utf-8'))

#identifica si la linea asm tiene un call
def identify_call_lines(line):
    if 'call' in line:
        return True
    return False

#Renoce la funcion
def rec_funct(field):
    for fun in functs_vulns:
        if fun in field:
            return fun
    return False

#separa los campos de las lineas con call, devolviendo los necesarios
def parse_call_line(line):
    fields = line.split()
    break_direction = fields[1][fields[1].index('<')+1:fields[1].index('>')]
    fun_name = rec_funct(fields[-1])
    return (fun_name, break_direction)


#mapea las funciones con los opcodes call y las agrega a la lista
def map_functions(gdb , funtions_dict):
    for fun in funtions_dict.keys():
        asm_funct_call[fun] = []
        gdb.sendline('disass {}'.format(fun))
        lines = gdb.recvlines(timeout=time_out)

        #print('-------------------------------------------------')
        #print_stdout(lines)
        #print('-------------------------------------------------')

        for line in lines:
            line = line.decode('utf-8')
            if identify_call_lines(line):
                x = parse_call_line(line)
                if x[0]:
                    asm_funct_call[fun].append(x)


#funcion general que realiza la fase de reconocimiento
def run_recognition_phase(executable, funtions_dict):
        gdb = exec_gdb(executable)
        gdb.recvlines(timeout=time_out)
        #print_stdout(gdb.recvlines(timeout=0.2))

        gdb.sendline('set height unlimited')
        gdb.recvlines(timeout=time_out)

        gdb.sendline('set width unlimited')
        gdb.recvlines(timeout=time_out)

        gdb.sendline('b main')
        gdb.recvlines(timeout=time_out)
        #print('>b main')
        #print_stdout(gdb.recvlines(timeout=0.2))

        gdb.sendline('run')
        gdb.recvlines(timeout=time_out)
        #print('>run')
        #print_stdout(gdb.recvlines(timeout=0.2))

        map_functions(gdb, funtions_dict)

        gdb.close()

        return asm_funct_call

if __name__ == '__main__':
    d = {'r':[], 'main':[]}
    run_recognition_phase('../x.out', d)
    print(asm_funct_call)
