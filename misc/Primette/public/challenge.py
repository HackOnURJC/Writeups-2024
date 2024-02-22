import random

LOST_VALUE = -1  # This is not the real seed value, we have lost it together with the programmer. We know it is < 1000
random.seed(LOST_VALUE)

first_primes_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
                     31, 37, 41, 43, 47, 53, 59, 61, 67,
                     71, 73, 79, 83, 89, 97, 101, 103,
                     107, 109, 113, 127, 131, 137, 139,
                     149, 151, 157, 163, 167, 173, 179,
                     181, 191, 193, 197, 199, 211, 223,
                     227, 229, 233, 239, 241, 251, 257,
                     263, 269, 271, 277, 281, 283, 293,
                     307, 311, 313, 317, 331, 337, 347, 349]


def n_bit_random(n):
    return random.randrange(2 ** (n - 1) + 1, 2 ** n - 1)


def get_low_level_prime(n, f):
    while True:
        pc = n_bit_random(n)
        for divisor in first_primes_list:
            if pc % divisor == 0 and divisor ** 2 <= pc:
                f.write("rnd: " + str(pc) + "\n")
                break
        else:
            return pc


def is_prime(number):
    '''
    We have lost the programmer that coded this function, we have no idea how to make it work
    '''


def find_prime():
    with open('output.txt', 'w') as f:
        while True:
            n = 1024
            prime_candidate = get_low_level_prime(n, f)
            if is_prime(prime_candidate):
                return prime_candidate


def encode(file_bytes):
    p = find_prime()
    final_bytes = b""
    for b_index in range(len(file_bytes)):
        if b_index % 2 == 0:
            final_bytes += ((8 + file_bytes[b_index]) % 256).to_bytes(1, 'little')
        else:
            final_bytes += (((file_bytes[b_index] * p) % 256) ^ 0xff).to_bytes(1, 'little')
    return final_bytes


def decode(file_bytes):
    '''
    Same programmer, same problem
    '''


if __name__ == '__main__':
    with open('flag.zip', 'rb') as file:
        result = encode(file_bytes=file.read())
        with open('flag.enc', 'wb') as r:
            r.write(result)
