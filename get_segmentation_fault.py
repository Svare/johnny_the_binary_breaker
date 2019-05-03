#!/usr/bin/python3

import subprocess

#time_out = 0.1

def get_breakpoint(info_list, binary_path):
	
	# info_list : ['main', '+25', 'strcpy', '5.', 'buffer', '0xffffc4a0', 'argv[1]', '0x61616161']
	# argv_num : 1

    chars = 10000 # Valor Maximo a Probar
    argv_num = info_list[-2].split('[')[1].split(']')[0].strip() # argv[#] con overflow
    
	# Busqueda Binaria

    while(True):

        process_args = [binary_path]
    
        for i in range(int(argv_num)):
            if i+1 == int(argv_num):
                process_args.append('b'*chars)
            else:
                process_args.append('a')

        res = subprocess.run(process_args)
        
        if res.returncode == -11:
            chars = chars // 2
        else:
            break

	# Ya que llege a un valor cercano con busqueda binaria me voy acercando de uno en uno
    
    while(True):

        process_args = [binary_path]
    
        for i in range(int(argv_num)):
            if i+1 == int(argv_num):
                process_args.append('b'*chars)
            else:
                process_args.append('a')

        res = subprocess.run(process_args)

        if res.returncode == -11:
             return chars
             break
        else:
            chars+=1

if __name__ == '__main__':

    print(get_breakpoint(['main', '+25', 'strcpy', '5.', 'buffer', '0xffffc4a0', 'argv[1]', '0x61616161'], '/home/ginger/poc/overflow'))
