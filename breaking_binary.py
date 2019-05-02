
from pwn import *
from functools import reduce
import sys

import recognition_phase

if __name__ == "__main__":

    d = {'main':[]}
    recognition_phase.run_recognition_phase('./buffer_overflow', d)
    print(recognition_phase.asm_funct_call)
