import json

from Crypto.Util.number import isPrime, long_to_bytes, bytes_to_long, getPrime
from pwn import process,remote
from library import JWS
from ecdsa.ecdsa import generator_384
from hashlib import sha256
from sage.all import QQ, Matrix, crt

#r = process(["python3","administration.py"])
r = remote("81.0.220.243", 1337)

def ecdsa_biased_nonce_attack(pubkey,msgs,r,s,B,N):
    d = None
    signatures = N
    n = generator_384.order()
    R = signatures + 2
    C = signatures + 2
    matrix = Matrix(QQ, R, C)

    msg_i = msgs
    r_i = r
    s_i = s

    s_inv_i = [pow(s_i[i],-1,n) for i in range(signatures)]
    t_i = [r_i[i]*s_inv_i[i] for i in range(signatures)]
    a_i = [msg_i[i]*s_inv_i[i] for i in range(signatures)]

    for i in range(signatures):
        matrix[i,i] = n

    for i in range(C-2):
        matrix[R-2, i] = t_i[i]
        matrix[R-1, i] = a_i[i]

    matrix[R-2,C-2] = (2**B) // n
    matrix[R-1,C-1] = 2**B

    solve_matrix = matrix.LLL(early_red=True, use_siegel=True)
    r1_inv = pow(r_i[0],-1,n)
    for row in solve_matrix:
        k1 = row[0]
        priv_key = r1_inv*((k1*s_i[0])- msg_i[0])
        test_pubkey = generator_384*priv_key
        possible = (test_pubkey.x(),test_pubkey.y())
        if possible == pubkey:
            print("ECDSA attack succesfull")
            print(f"Private Key: {priv_key % n}")
            d = priv_key % n
            break
    return d



def get_token(i):
    r.recvuntil(b'[*]Option: ')
    r.sendline(b'2')
    r.recvuntil(b'Username: ')
    r.sendline(str(i).encode())
    r.recvuntil(b'Alg: ')
    r.sendline(b'ESBLK')
    token = r.recvline().replace(b'\n', b'')
    return token.decode()


def get_msg_hash(token):
    header, payload,_ = JWS.load_token(token)
    sign_input = b".".join([header, payload]) 
    token_hash = bytes_to_long(sha256(sign_input).digest())
    return token_hash


def get_signature(token):
    _,_,signature = JWS.load_token(token)
    bytes_r,bytes_s = signature.split(b'&&')
    r = bytes_to_long(bytes_r)
    s = bytes_to_long(bytes_s)
    return (r,s)


def get_pubkey(token):
    r.recvuntil(b'[*]Option: ')
    r.sendline(b'1')
    r.recvuntil(b'Token, please: ')
    r.sendline(token.encode())
    r.recvuntil(b'This is your public key: \n')
    pkX,pkY = map(int,r.recvline().strip().split())
    return (pkX,pkY)


def create_payload():
    payload = dict()
    payload['username'] = "HugoBond"
    payload['dfh'] = getPrime(200)
    payload['iat'] = payload['dfh'] + 1
    payload['status'] = "Rector"
    return payload



def get_flag(priv_key):
    jws = JWS(long_to_bytes(int(priv_key)))
    res = []
    modulus = []
    for i in range(4):
        payload = create_payload()
        modulus.append(payload['dfh'])
        new_token = jws.encode(json.dumps(payload), "ES512")
        r.recvuntil(b'[*]Option: ')
        r.sendline(b'1')
        r.recvuntil(b'Token, please: ')
        r.sendline(new_token.encode())
        r.recvuntil(b'Rector, this belongs to you: ')
        encoded_flag = int(r.recvline().replace(b'\n', b''))
        res.append(encoded_flag)
    
    # x = (p + 1)^flag mod p² = p*flag + 1 mod p² --> flag = (x-1) / p
    target = [(x-1)//t for x,t in zip(res,modulus)]
    flag = crt(target,modulus)
    return flag
        

def main():
    data = {"hashes":[], "rs":[], "ss":[]}
    token = None
    Nsig = 27
    for i in range(Nsig):
        token = get_token(i)
        data["hashes"].append(get_msg_hash(token))
        r_sig,s_sig = get_signature(token)
        data["rs"].append(r_sig)
        data["ss"].append(s_sig)

    pubkey = get_pubkey(token)
    priv_key = ecdsa_biased_nonce_attack(pubkey,data["hashes"], data["rs"], data["ss"], 368, Nsig)
    if not priv_key:
        print("Attack Failed.")
        exit()

    flag = get_flag(priv_key)
    if flag:
        print(f"Flag recovered: {long_to_bytes(flag).decode()}")
        
    else:
        print("Flag recovery FAILED.")
        

if __name__ == '__main__':
    main()
