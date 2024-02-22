from math import gcd
import rsa
from sympy import mod_inverse
from Crypto.Util.number import long_to_bytes

#Read from file and get params
with open('output.txt', 'r') as archivo:
    lineas = archivo.readlines()
    N1 = int(lineas[0][4:])
    e1 = int(lineas[1][4:])
    e2 = int(lineas[2][4:])
    c1 = int(lineas[3][4:])
    c2 = int(lineas[4][4:])
    flag_enc = int(lineas[5][10:])



#Froce-brute r and get N=p*q
Nsol= 0
for i in range(pow(2, 23) +1, pow(2, 24), 2):
    if (gcd(N1, i) != 1):
        Nsol= N1//i
        break

#pow ecuations their respective oposite exponents
c1mod = pow(c1, e2, Nsol)
c2mod = pow(c2, e1, Nsol)

#Operate between ecuatios to get eq2=pow(k*q, e1*e2, N)
eq2 = (c2mod * pow(7,e1*e2, Nsol) -c1mod* pow(5, e1*e2, Nsol)) % Nsol

#Do gcd between eq2 and N to get q and get p trivially
qsol= gcd(eq2, Nsol) 
psol = Nsol // qsol

print (f'\n\n\np: {psol}\nq: {qsol}\n')

#Get the rsa private key and decrypt the flag

flag_dec = pow(flag_enc, mod_inverse(0x10001, (psol -1)*(qsol-1)), Nsol)
flag_dec = long_to_bytes(flag_dec)
print(flag_dec.decode('utf8'))
