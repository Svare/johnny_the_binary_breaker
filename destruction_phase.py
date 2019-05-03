#!/usr/bin/python3

from pwn import *
from functools import reduce

import sys

time_out = 0.1
dict_of_bkpnts = {}
ascii_character = 'd'
last = '2'

#ejecuta gdb
def exec_gdb(file_name):
    #return process(['/usr/bin/gdb', file_name , '-q'])
    return process('/usr/bin/gdb {} -q'.format(file_name), shell=True)

#imprime con utf-8 las lineas adquiridas desde recvlines
def print_stdout(lines):
    for line in lines:
        print(line.decode('utf-8'))

def raw_to_str(byte_array_list):
    return reduce(lambda x,y: x + '\n'.encode() + y, byte_array_list).decode()


#anade breakpoint a todas las posibles funciones vulnerables
def set_breakpoints(gdb, functs_dict):
    n_brk = 2
    for key in functs_dict.keys():
        for brk in functs_dict[key]:
            #print('b *main{}'.format(brk[1]))
            gdb.sendline('b *{}{}'.format(key,brk[1]))
            line = gdb.recvlines(timeout=time_out)[0].decode('utf-8')
            line = line.split()[-1]
            #print_stdout(gdb.recvlines(timeout=time_out))
            dict_of_bkpnts[str(n_brk)] = [key,brk[1],brk[0],line]
            n_brk += 1
    print('\n\nBreakpoints:: \n')
    gdb.sendline('info b')
    print(raw_to_str(gdb.recvlines(timeout=time_out)))

def get_destination_var(string):
    return string[string.find('(')+1:string.rfind(')')].split(',')[0].strip()

def get_origin_var(string):
    return string[string.find('(')+1:string.rfind(')')].split(',')[1].strip()

def n_argument(n, string):
    return string[string.find('(')+1:string.rfind(')')].split(',')[n].strip()

def get_memory_address(string):
    return string.strip().split()[-1]

def detect_buffer_overflow(lines):
    for line in lines:
        line = line.decode('utf-8')
        #print('----- >' + line)
        if 'Segmentation fault' in line:
            return True
    return False

def break_it(gdb):
    for i in dict_of_bkpnts.keys():
        gdb.sendline('c')
        resp = gdb.recvlines(timeout=time_out)
        print('Primer breakpoint:: \n')
        print(raw_to_str(resp))
        #print_stdout(resp)
        #print('Enviado a identif --->  '+resp[0].decode('utf-8') )
        #print('----------------------------------------------------------')
        #print_stdout(resp)
        #print('----------------------------------------------------------')

        if detect_buffer_overflow(resp):
            return resp

        print_stdout(resp)

        bk = resp[2].decode('utf-8').split()[1].replace(',','')

        #print("Break -->  " + bk )
        identif = get_destination_var(resp[3].decode('utf-8'))
        origin = get_origin_var(resp[3].decode('utf-8'))
        #print("Identificador " + identif)
        #print(origin)
        gdb.sendline('x/x {}'.format(origin))
        resp = gdb.recvlines(timeout=time_out)
        print_stdout(resp) ####################################################
        valuee = resp[0].decode('utf-8').split()[2]
        #print(valuee)
        gdb.sendline('p &{}'.format(identif))
        resp = gdb.recvlines(timeout=time_out)
        #print_stdout(resp)
        mem = get_memory_address(resp[0].decode('utf-8'))
        #print(mem)
        dict_of_bkpnts[bk].extend((identif,mem, origin, valuee))
        last = bk
    return False

def break_it_(gdb):

    global ascii_character
    global last

    print('\nBreakpoints:: \n')
    print(dict_of_bkpnts)

    # En este punto estamos parados en el break del main necesitamos darle un continue (c) para
    # poder pasar a situarnos a el primer breakpoint de la primera funcion vulnerable.

    gdb.sendline('c') # Avanzar del breakpoint del main

    for i in dict_of_bkpnts.keys():
        
        resp = gdb.recvlines(timeout=time_out)
        print(raw_to_str(resp))
        bk = resp[-2].decode('utf-8').split()[1].replace(',', '') # Numero de breakpoint (indice de nuestro diccionario)

        if detect_buffer_overflow(resp):
            return resp

        if(dict_of_bkpnts[bk][2] == 'scanf'):

            raw = raw_to_str(resp).split('\n')
            destination = n_argument(1, raw[-1])

            gdb.sendline('p &{}'.format(destination))
            resp = gdb.recvlines(timeout=time_out)
            raw = raw_to_str(resp).split('\n')
            memory_address = get_memory_address(raw[0])

            argv = 'STDIN'

            break_vector = ascii_character

            ascii_character = chr(ord(ascii_character) + 1)
            dict_of_bkpnts[bk].extend([destination, memory_address, argv, break_vector])
            
            gdb.sendline('c')
            gdb.sendline(ascii_character*10)

            last = bk

        elif(dict_of_bkpnts[bk][2] == 'gets'):
            print('gets')

        elif(dict_of_bkpnts[bk][2] == 'strcpy'):
            
            raw = raw_to_str(resp).split('\n')
            destination = n_argument(0, raw[-1])

            argv = n_argument(1, raw[-1])

            gdb.sendline('p &{}'.format(destination))
            resp = gdb.recvlines(timeout=time_out)
            raw = raw_to_str(resp).split('\n')
            memory_address = get_memory_address(raw[0])

            gdb.sendline('x/x {}'.format(argv))
            resp = gdb.recvlines(timeout=time_out)
            raw = raw_to_str(resp).split('\n')
            print(raw)

            break_vector = chr(int(raw[-1][-2:], 16))

            dict_of_bkpnts[bk].extend([destination, memory_address, argv, break_vector])
            
            gdb.sendline('c')
            
            last = bk
    
def set_argvs(letters_list, argv_len, gdb):

    argvs = 'r' + reduce(lambda x,y: x + y, map(lambda x: ' ' + x*argv_len, letters_list))
    
    # con
    # letters_list = ['a', 'b', 'c']
    # argv_len = 5
    # argvs generaria 'r aaaaa bbbbb ccccc'

    ascii_character = chr(ord(letters_list[-1]) + 1)

    gdb.sendline(argvs)
    gdb.recvlines(timeout=time_out)

#funcion general que realiza la fase de destruccion
def destruction_phase(executable, functs_dict):

    gdb = exec_gdb(executable)
    gdb.recvlines(timeout=time_out)

    gdb.sendline('set height unlimited')
    gdb.recvlines(timeout=time_out)

    gdb.sendline('set width unlimited')
    gdb.recvlines(timeout=time_out)

    gdb.sendline('b main')
    gdb.recvlines(timeout=time_out)

    set_argvs(['a', 'b', 'c'], 900, gdb) # Especificando argvs

    set_breakpoints(gdb, functs_dict)

    gdb.sendline('run')
    gdb.recvlines(timeout=time_out)

    resp = break_it_(gdb)

    if not resp:
        gdb.sendline('c')
        resp = gdb.recvlines(timeout=time_out)
        if not detect_buffer_overflow(resp):
            print("El programa no es vulnerable")
            sys.exit(0)

    gdb.close()

    return dict_of_bkpnts[last]

if __name__ == '__main__':
    d = {'main': [('strcpy', '+25')]}
    print(destruction_phase('./buffer_overflow', d))
    print(dict_of_bkpnts)
