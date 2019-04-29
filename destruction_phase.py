#!/usr/bin/python3
from pwn import *
from functools import reduce
import sys

time_out = 0.1
dict_of_bkpnts = {}
ascii_character = '0'

#ejecuta gdb
def exec_gdb(file_name):
    return process(['/usr/bin/gdb', file_name , '-q'])

#imprime con utf-8 las lineas adquiridas desde recvlines
def print_stdout(lines):
    for line in lines:
        print(line.decode('utf-8'))

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

def get_destination_var(string):
    return string[string.find('(')+1:string.rfind(')')].split(',')[0].strip()

def get_memory_address(string):
    return string.strip().split()[-1]

def detect_buffer_overflow(lines):
    for line in lines:
        line = line.decode('utf-8')
        print('----- >' + line)
        if 'Segmentation fault' in line:
            return True
    return False

def break_it(gdb):
    for i in dict_of_bkpnts.keys():
        gdb.sendline('c')
        resp = gdb.recvlines(timeout=time_out)
        #print_stdout(resp)
        #print('Enviado a identif --->  '+resp[0].decode('utf-8') )
        if detect_buffer_overflow(resp):
            return resp
        bk = resp[2].decode('utf-8').split()[1].replace(',','')
        #print("Break -->  " + bk )
        identif = get_destination_var(resp[3].decode('utf-8'))
        #print("Identificador " + identif)
        gdb.sendline('p &{}'.format(identif))
        resp = gdb.recvlines(timeout=time_out)
        #print_stdout(resp)
        mem = get_memory_address(resp[0].decode('utf-8'))
        #print(mem)
        dict_of_bkpnts[bk].extend((identif,mem))
    return False

def set_argvs(letters_list, argv_len, gdb):

    # letters_list = ['a', 'b', 'c']
    # argv_len = 5

    argvs = 'r' + reduce(lambda x,y: x + y, map(lambda x: ' ' + x*argv_len, letters_list))

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

    set_argvs(['a', 'b', 'c'], 500, gdb) # Especificando argvs

    set_breakpoints(gdb, functs_dict)

    gdb.sendline('run')
    #print_stdout(gdb.recvlines(timeout=time_out))
    gdb.recvlines(timeout=time_out)

    resp = break_it(gdb)
    if not resp:
        gdb.sendline('c')
        resp = gdb.recvlines(timeout=time_out)
        if not detect_buffer_overflow(resp):
            print("El programa no es vulnerable")
            sys.exit(0)

    resp = resp[-1].decode('utf-8').split()[0]

    print('Rompio con la direccion ' + resp)

    gdb.close()


if __name__ == '__main__':
    d = {'main': [('strcpy', '+25')]}
    destruction_phase('../x.out',d)
    print(dict_of_bkpnts)
