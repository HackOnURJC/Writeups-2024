# Solver Coquette

Para resolver este challenge, simplemente hay que hacer fuerza bruta sobre los bytes cifrados y decodificar la imagen.

El código que lo resuelve se puede encontrar en el fichero solver.py y a continuación:

```python3

def brute_force(b):
    for i in range(256):
        if (i % 256) ^ 0xff == b:
            return i


def decode(file_bytes):
    original_bytes = b""
    for b_index in range(len(file_bytes)):
        if b_index % 2 == 0:
            original_bytes += ((file_bytes[b_index] - 8) % 256).to_bytes(1, 'little')
        else:
            decoded_byte = brute_force(file_bytes[b_index]).to_bytes(1, 'little')
            original_bytes += decoded_byte

    with open('solved.png', 'wb') as s:
        s.write(original_bytes)


if __name__ == '__main__':
    with open('flag.enc', 'rb') as e:
        decode(e.read())
```
