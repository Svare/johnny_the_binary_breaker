
import re
from sys import argv

if __name__ == "__main__":

    r = re.compile('main\s*\(\s*.*char\s*(?:\*\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\[\s*\]|\*\s*\*\s*([a-zA-Z_][a-zA-Z0-9_]*))[^)]*\)')

    with open(argv[1], 'r') as archivo:
        for line in archivo.readlines():
            result = re.findall(r, line)
            if result:
                print(result)