#!/usr/bin/python3
import sys

def print_error():
    print('ERROR: The recognition The recognition phase failed')
    sys.exit(1)

def compare_dicts(dict1, dict2):
    if len(dict1) != len(dict2):
        print_error()

    keys1 = sorted(dict1.keys())
    keys2 = sorted(dict2.keys())

    if not (keys1 == keys2):
        print_error()

    for key in keys1:
        if (len(dict1[key]) != len(dict2[key])) or len(dict1[key]) == 0 or len(dict2[key]) == 0:
            del dict1[key]
            del dict2[key]
            continue

        for i in range(len(dict1[key])):
            if dict1[key][i] != dict2[key][i][0]:
                print_error()

    return (dict1,dict2)

if __name__ == '__main__':
    d1 = {'r':[],'main':['strcpy','strcpy','gets','scanf']}
    d2 = {'r':[],'main':[('strcpy',32),('strcpy',35),('gets',45),('scanf',50)]}
    print(compare_dicts(d1, d2))
