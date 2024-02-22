from tqdm import tqdm
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from itertools import combinations, product

from hashlib import sha256

with open("/home/bond/ctfs/hackOn/insane/dist/output.txt") as f:
    exec(f.read())


def recover_generator(a,b,n):
    # recover G
    # Gy^2 = Gx^3 + a*Gx + b (mod n^2)
    # Gy^2 - Gx^3 ~ 256*3 bits
    # Gx ~ 256 bits
    # n^2 ~ 431*2*2 bits
    L = matrix([[n ^ 2, 0, 0], [a, 1, 0], [b, 0, 1]])
    K = 2 ^ 1024
    Q = matrix.diagonal([K // 2 ^ (32 * 8 * 3), K // 2 ^ (32 * 8), K // 1])
    L *= Q
    L = L.LLL()
    L /= Q
    Gx = L[0][1]
    Gy2 = L[0][0] + Gx ^ 3
    assert Gy2 % (n ^ 2) == (Gx ^ 3 + a * Gx + b) % (n ^ 2)
    Gy = sorted(GF(p)(Gy2).sqrt(all=True))[0]
    return Gx,Gy

def recover_mod(point1, point2, point3):
    #https://hackmd.io/@mystiz/uiuctf-2020-nookcrypt stolen equation
    x1, y1 = point1
    x2, y2 = point2
    x3, y3 = point3
    return (y1 ^ 2 - y2 ^ 2 - x1 ^ 3 + x2 ^ 3) * (x2 - x3) - (y2 ^ 2 - y3 ^ 2 - x2 ^ 3 + x3 ^ 3) * (x1 - x2)


def ecc(a, b, x, y):
    return y ^ 2 - (x ^ 3 + a * x + b)


def solve_lin(f):
    return ZZ(-f[0] / f[1])


def dlog(G, Y, p, od):
    E = EllipticCurve(Qp(p, prec=2), [a, b])
    G = E([ZZ(x) % p**2 for x in G.xy()])
    Y = E([ZZ(x) % p**2 for x in Y.xy()])

    def phi(P):
        x, y = (P * od).xy()
        return x / y

    return (phi(Y) / phi(G)).lift()

def dlogn(G, Y):
    xp = dlog(G, Y, p, odp)
    xq = dlog(G, Y, q, odq)
    return crt([xp, xq], [p, q])


# Recover modulus from more than 3 points 
n = reduce(gcd, [recover_mod(*ps) for ps in zip(points, points[1:], points[2:])]).sqrt()
print(f"N = {n}")

# Recover a and b
P.<a, b> = Zmod(n**2)[]
f = ecc(a, b, *points[0])
g = ecc(a, b, *points[1])
h1 = f.sylvester_matrix(g, b).det().univariate_polynomial()
h2 = f.sylvester_matrix(g, a).det().univariate_polynomial()
a = solve_lin(h1)
b = solve_lin(h2)
print(f"Parameter a recovered: {a}")
print(f"Parameter b recovered: {b}")

E = EllipticCurve(Zmod(n), [a, b])
#Similar technique to ECM, factor n using elliptic-curve factorization method
for i in range(2, 100):
    if master % i == 0:
        try:
            E(*points[0]) * int(master // i)
        except ZeroDivisionError as ex:
            v = ZZ(str(ex).split("Inverse of ")[1].split(" does not exist")[0])
            p = gcd(v, n)
            break

q = n // p
assert p * q == n
print(f"p = {p}\nq = {q}")

Gx,Gy = recover_generator(a,b,n)
print(f"{Gx = }")
print(f"{Gy = }")

E = EllipticCurve(Zmod(n**2), [a, b])
points = [E(x) for x in points]
G = E(Gx, Gy)

odp = EllipticCurve(GF(p), [a, b]).order()
odq = EllipticCurve(GF(q), [a, b]).order()
print(f"{odp = }")
print(f"{odq = }")
coefficients = [dlogn(G, Y) for Y in tqdm(points)]

# Decrypt Flag
KEY = sha256(str(sum(coefficients)).encode()).digest()
cipher = AES.new(KEY, AES.MODE_CBC, b"iseeyou!"*2)
flag = cipher.decrypt(bytes.fromhex(enc_flag))
print(f"Flag: {unpad(flag, 32)}")

