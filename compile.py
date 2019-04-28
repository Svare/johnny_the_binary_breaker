#!/usr/bin/python3
import subprocess
import os
import sys


def file_exist(file_name):
    if os.path.isfile(file_name):
        return True
    return False


def create_out_file_name(file_name):
    if not '.c' in file_name:
        print('ERROR: Need a C file')
        sys.exit(1)
    name = file_name.replace('.c','.out')
    return name


def compile_file(file_name):
    if not file_exist(file_name):
        print('ERROR: The file does not exists')
        sys.exit(1)

    out_fl_name = create_out_file_name(file_name)

    compile_process = subprocess.run(['gcc', file_name, '-o', out_fl_name],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if compile_process.returncode != 0 or (not file_exist(out_fl_name)):
        print('ERROR: The code could not be compiled')
        print('-------------- Error message --------------')
        print(compile_process.stderr.decode('utf-8'))
        print('------------------------------------------')
        sys.exit()


if __name__ == '__main__':
    compile_file('p.c')
