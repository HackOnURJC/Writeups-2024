opcodes = {
    b'\x00' : 'print',
    b'\x01' : 'read',
    b'\x02' : 'add',
    b'\x03' : 'sub',
    b'\x04' : 'xor',
    b'\x05' : 'jmp',
    b'\x06' : 'je',
    b'\x07' : 'jne',
    b'\x08' : 'jg',
    b'\x09' : 'jl',
    b'\x0a' : 'mv',
    b'\x0b' : 'li',
    b'\x0c' : 'ld',
    b'\x0d' : 'st',
    b'\x0e' : 'hlt',
    b'\x0f' : 'even' 
}

registers = {
    b'\x00' : 'rax',
    b'\x01' : 'rdi',
    b'\x02' : 'rsi',
    b'\x03' : 'rdx',
    b'\x04' : 'rcx',
    b'\x05' : 'r8',
    b'\x06' : 'r9',
    b'\x07' : 'r10',
    b'\x08' : 'r11',
    b'\x09' : 'rsp',
    b'\x0a' : 'rbx',
    b'\x0b' : 'rbp',
    b'\x0c' : 'r12',
    b'\x0d' : 'r13',
    b'\x0e' : 'r14',
    b'\x0f' : 'r15' 
}

def generateLine(content):
    if content[3] in opcodes:
        op = opcodes[content[3]]
        
        if op == "print" or op == "read":
            if content[2] in registers:
                reg = registers[content[2]]
                line = f"{op} {reg}"
            
        if op == "add" or op == "sub" or op == "xor" or op == "mv":
            if content[2] in registers and content[1] in registers:
                reg1, reg2 = registers[content[2]], registers[content[1]]
                line = f"{op} {reg1} {reg2}"

        if op == "jmp":
            line = f"{op} {content[1]}{content[2]}"

        if op == "je" or op == "jne" or op == "jg" or op == "jl":
            if content[2] in registers and content[1] in registers:
                reg1, reg2 = registers[content[2]], registers[content[1]]
                line = f"{op} {reg1} {reg2} {content[3]}"

        if op == "li" or op == "ld" or op == "st":
            if content[2] in registers:
                reg1 = registers[content[2]]
                line = f"{op} {reg1} {content[1]}{content[0]}"

        if op == "hlt":
            line = f"{op}"

        if op == "even":
            if content[2] in registers and content[1] in registers:
                reg1, reg2 = registers[content[2]], registers[content[1]]
                line = f"{op} {reg1} {reg2}"              

    else:
        line = f"{content[3]}{content[2]}{content[1]}{content[0]}"

    return line

# Files
file = "file"
out_file = "asm"
deciphered = "deciphered"
deciphered_asm = "deciphered_asm"

# Variables
byte = bytearray([0x51, 0x41, 0x31, 0x21])
counter = 0

# Read the content and parse
with open(file, "rb") as f:
    content = [f.read(1) for _ in range(4)] 
    while content[0]:
        with open(out_file, "a") as r:
            line = generateLine(content)
            r.write(line + "\n")

        content = [f.read(1) for _ in range(4)]

# Read all the content
with open(file, "rb") as fd:
    buffer = bytearray(fd.read())

# Decipher the content
for i in range(len(buffer)):
    buffer[i] ^= byte[i % 4]

# Write the content into a file
with open(deciphered, "wb") as r:
    r.write(buffer)

# Read the content and parse
with open(deciphered, "rb") as f:
    content = [f.read(1) for _ in range(4)] 
    while content[0]:
        with open(deciphered_asm, "a") as r:
            line = generateLine(content)
            r.write(line + "\n")

        content = [f.read(1) for _ in range(4)]

ciphered_flag = bytearray([0xa7, 0x5a, 0xa5, 0x00, 0x97, 0x6c, 0x63, 0x55, 0x92, 0x50, 0x9b, 0x56, 0x96, 0x58, 0x64, 0x5d,
                           0x9a, 0x6c, 0xa6, 0x47, 0xa5, 0x46, 0x96, 0x47, 0x92, 0x45, 0x94, 0x5f, 0xa8, 0x00, 0xa6, 0x6c])

original_flag = bytearray()

for i in range(len(ciphered_flag)):
    if (i % 2) == 0:
        original_flag.append(ciphered_flag[i] - 0x33)
    else:
        original_flag.append(ciphered_flag[i] ^ 0x33)

# Convertir los bytes a una cadena ASCII
original_flag_str = original_flag.decode()

print("Original Flag:", original_flag_str)