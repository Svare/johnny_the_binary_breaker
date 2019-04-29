#!/usr/bin/python3
from pwn import *

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
    n_brk = 1
    for key in functs_dict.keys():
        for brk in functs_dict[key]:
            #print('b *main{}'.format(brk[1]))
            gdb.sendline('b *main{}'.format(brk[1]))
            line = gdb.recvlines(timeout=time_out)[0].decode('utf-8')
            line = line.split()[-1]
            #print_stdout(gdb.recvlines(timeout=time_out))
            dict_of_bkpnts[str(n_brk)] = [key,brk[1],brk[0],line]
            n_brk += 1

def break_it(gdb):
    for i in range(1,len(dict_of_bkpnts)+1):
        print('c')
        gdb.sendline('c')
        print_stdout(gdb.recvlines(timeout=time_out))
        if (dict_of_bkpnts[str(i)][2] == 'scanf') or (dict_of_bkpnts[str(i)][2] == 'gets'):
            x = input()
            gdb.sendline(x*9)
            print_stdout(gdb.recvlines(timeout=time_out))


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

    set_breakpoints(gdb, functs_dict)

    gdb.sendline('run')
    print_stdout(gdb.recvlines(timeout=time_out))

    #break_it(gdb)

    
    gdb.close()


if __name__ == '__main__':
    d = {'r': [], 'main': [('scanf', '+35'), ('strcpy', '+51'), ('gets', '+76'), ('strncpy', '+94')]}
    destruction_phase('../x.out',d)
    print(dict_of_bkpnts)
