
import re

if __name__ == "__main__":

    MAX_INT = 0

    integers = [
        re.compile(r'#define\s+(?:[a-zA-Z_][a-zA-Z0-9_]*)\s+([0-9]+)\s*'),
        re.compile(r'(?:[a-zA-Z_][a-zA-Z0-9_]*)\s*\=\s*([0-9]+)\s*[,;]')
    ]

    line = ' char sdsdfafdafdas = "241242143"; hola = 45, jesus = 12341234; char jaja = "666666"'

    while '"' in line:
            line = line[:line.index('"')] + line[line.index('"', int(line.index('"') + 1)) + 1 :]
            

    for regex in integers:

        print(type(line))

        result = re.findall(regex, line)

        print(result)

        if result:
            for value in result:
                MAX_INT = int(value) if (int(value) > MAX_INT) else MAX_INT
            break
        
    print(MAX_INT)