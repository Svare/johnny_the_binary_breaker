
import re

def get_functions_calls(full_file):

    stack = []
    global_index = 0
    func_calls_list = []

    func_call = re.compile(r'(?:[a-zA-Z_][a-zA-Z0-9_]*)\s*\(')

    func_calls = re.findall(func_call, full_file)
    string = full_file

    for match in func_calls:

        global_index = string.find(match)   # Valor inicial principio de la primera llamada a funcion
        global_index += len(match)          # Se posiciona en el caracter despues de (
        i = global_index
        buffer = ''
        stack.append('(')

        while True:

            if string[i] == '(':
                stack.append('(')
            elif string[i] == ')':
                stack.pop()
            
            buffer+=string[i]
            i+=1

            if len(stack) == 0:
                args = buffer
                break
        
        string = string[global_index:]

        if '(' in buffer[:-1]:
            args = [buffer[:-1]]
        else:
            args = list(map(lambda x: x.strip(), buffer[:-1].split(',')))
        
        func_calls_list.append((match.split('(')[0].strip(), args))
    
    return func_calls_list

if __name__ == "__main__":
    
    xxx = '''
	           if (argv[0]==NULL) usage();

    // check for a trailing dot
    strcpy(argv0,argv[0]);
    if (argv0[strlen(argv[0])-1]=='.') argv0[strlen(argv[0])-1]=0;

    printf("Tracing to %s[%s] via %s, maximum of %d retries\n",
	argv0,rr_types[global_querytype],server_name,global_retries);

    srandom(time(NULL));
        '''
    
    print(get_functions_calls(xxx))
    
   