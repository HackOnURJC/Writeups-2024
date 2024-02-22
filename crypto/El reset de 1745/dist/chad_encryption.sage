from Crypto.Util.number import  getPrime
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
from hashlib import sha256

def hide_flag_between_reptilians(key,plaintext):
    iv = b"iseeyou!"*2
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plaintext, 32))
    return ciphertext.hex()


def get_master_parameters():
    p = getPrime(431)
    q = getPrime(431)
    Gx, Gy = randrange(2**256,2**257), randrange(2**256,2**257)
    a = randint(2, (p*q)**2)
    b = (Gy**2 - Gx**3 - a*Gx) % (p*q)**2
    return (a,b,p,q,(Gx,Gy))


def third_dimension_ecc(G,N):
    garbage = [randint(1,N) for _ in range(32)]
    secret_array = [garbage[i] * G for i in range(32)]
    print(f"In your dimension you are able to see this: {[x.xy() for x in secret_array]}")
    return sha256(str(sum(garbage)).encode()).digest()


def main():
    a,b,p,q, G = get_master_parameters()
    N = p*q
    E = EllipticCurve(Zmod(N) , [a,b])
    B = E(G)
    master_eye = int(E.change_ring(GF(q)).order()*E.change_ring(GF(p)).order())
    point2inf = E(0,1,0)
    assert master_eye*B == point2inf
    print(f"The Master Eye is granted to you: {master_eye}")

    EM = EllipticCurve(Zmod(N**2) , [a,b])
    with open("flag.txt","rb") as f:
        FLAG = f.read()
    KEY = third_dimension_ecc(EM(G),N)
    print("enc_flag = ",hide_flag_between_reptilians(KEY, FLAG))
    

if __name__ == "__main__":
    main()