#!/usr/bin/python3

from pwn import *
time_out = 0.1

def get_break_point(info_list):

    chars = 10000
    argv_num = info_list[6].split('[')[1].split(']')[0].strip()
    
    while(True):

        process_args = ['/root/poc/argv']
    
        for i in range(int(argv_num)):
            if i+1 == int(argv_num):
                process_args.append('b'*chars)
            else:
                process_args.append('a')

        res = subprocess.run(process_args, capture_output=True)
        
        if res.returncode == -11:
            chars = chars // 2
        else:
            break
    
    while(True):

        process_args = ['/root/poc/argv']
    
        for i in range(int(argv_num)):
            if i+1 == int(argv_num):
                process_args.append('b'*chars)
            else:
                process_args.append('a')

        res = subprocess.run(process_args, capture_output=True)

        if res.returncode == -11:
             print(chars)
             break
        else:
            chars+=1

if __name__ == '__main__':

    get_break_point([0, 1, 2, 3, 4, 5, ' argv[ 2 ] '])
