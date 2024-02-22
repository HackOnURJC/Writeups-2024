from Crypto.Util.number import getPrime, bytes_to_long
import random


flag='HackOn{testing_flag}'

p = getPrime(1024)
q = getPrime(1024)
r = getPrime(24)

N1 = p * q * r
N = p * q


e1 = 34456075732829756714431696264844933736161425428678777444326530245267175496676105
e2 = 66213320562378389542956020292848603326457400359492442893037745994906793456536650


c1 = pow(7 * p + random.randint(N,N1) * q, e1, N)
c2 = pow(5 * p + random.randint(2,N) * q, e2, N)

print (f'N1: {N1}\ne1: {e1}\ne2: {e2}\nc1: {c1}\nc2: {c2}')

flag_enc= pow(bytes_to_long(flag.encode()),0x10001,N)
print (f"flag_enc: {flag_enc}")
