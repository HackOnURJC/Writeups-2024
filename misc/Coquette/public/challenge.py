def encode(file_bytes):
    final_bytes = b""
    for b_index in range(len(file_bytes)):
        if b_index % 2 == 0:
            final_bytes += ((8 + file_bytes[b_index]) % 256).to_bytes(1, 'little')
        else:
            final_bytes += ((file_bytes[b_index] % 256) ^ 0xff).to_bytes(1, 'little')
    return final_bytes


def decode(file_bytes):
    '''
    Sorry boss, we have no idea how to implement this function, we have failed you -.-'
    '''


if __name__ == '__main__':
    with open('flag.png', 'rb') as file:
        result = encode(file_bytes=file.read())
        with open('flag.enc', 'wb') as r:
            r.write(result)
