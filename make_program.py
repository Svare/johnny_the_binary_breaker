#!/usr/bin/python3

import subprocess
import os
import sys

def file_exist(file_name):
    if os.path.isfile(file_name):
        return True
    return False

def do_make(dir_name):

    os.chdir(dir_name)

    if not file_exist('configure'):
        print('ERROR: The configure file was not found')
        sys.exit(1)

    # compile_process = subprocess.run( './configure' ,stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # if compile_process.returncode != 0:
    #     print('ERROR: The code could not be configured')
    #     print('-------------- Error message --------------')
    #     print(compile_process.stderr.decode('utf-8'))
    #     print('------------------------------------------')
    #     sys.exit()

    if not file_exist('Makefile'):
        print('ERROR: The Makefile file was not found')
        sys.exit(1)

    compile_process = subprocess.run( 'make' ,stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if compile_process.returncode != 0:
        print('ERROR: The code could not be configured')
        print('-------------- Error message --------------')
        print(compile_process.stderr.decode('utf-8'))
        print('------------------------------------------')
        sys.exit()

    print('*** make succeed ***')


if __name__ == '__main__':
    do_make('/root/Downloads/gdb-8.2')
