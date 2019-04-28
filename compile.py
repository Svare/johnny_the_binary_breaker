#!/usr/bin/python3
import subprocess
import os
import sys

compile_flags = ['gcc' ,'-no-pie','-ggdb','-m32', '-fno-pic', '-z', 'execstack', '-mpreferred-stack-boundary=2', '-fno-stack-protector', '-o']


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

    compile_flags.insert(2, file_name)
    out_fl_name = create_out_file_name(file_name)
    compile_flags.append(out_fl_name)

    #compile_process = subprocess.run(['gcc', file_name, '-o', out_fl_name],
    #    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    compile_process = subprocess.run( compile_flags ,stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if compile_process.returncode != 0 or (not file_exist(out_fl_name)):
        print('ERROR: The code could not be compiled')
        print('-------------- Error message --------------')
        print(compile_process.stderr.decode('utf-8'))
        print('------------------------------------------')
        sys.exit()

    print('Compilation Succeed')

if __name__ == '__main__':
    compile_file('../x.c')
