# Jorge Wants a Token

### Contenidos del reto

- ECDSA
- Retículos
- JWT
- Aritmética Modular
- Binomio de Newton Modular
- Teorema Chino del Resto

## Primera parte - Forge Tokens

El objetivo de este reto es obtener un token con el `status` de `Rector`

```python
if status == "Rector" and type(dfh) == int == type(iat):
            flag = bytes_to_long(FLAG.encode())
```

El servidor permite dos opciones principales **iniciar sesión** y **registrarte.** Para iniciar sesión es necesario un token `JWT`. El servidor importa una librería con una clase **`JWS`** que gestiona estos tokens. Esta librería soporta 3 algoritmos distintos de firmas:

1. **HSMAC256**. Hash hmac con clave privada.
2. **ES512**:
    
    Este algoritmo utiliza ECDSA para generar las firmas y el hash SHA512 para generar los nonces.  
    
3. **ESBLK**:
    
    Es igual al anterior pero los nonces se generan con el algoritmo BLAKE2b y trunca el output a 368 bits. Esta generación de nonces no es segura, ya que se tienen que generar de forma aleatoria entre 1 y el orden de la curva.
    

```python
hash = blake2b(digest_size=46)
hash.update(key + urandom(16))
nonce = bytes_to_long(hash.digest())
sign = self.privKey.sign(bytes_to_long(sha256(input.encode()).digest()), nonce)
```

Otra parte importante es que cada vez que nos conectamos al servidor se genera una clave privada nueva y solo se puede interactuar como máximo 32 veces.

```python
if __name__ == '__main__':
    jws = JWS(long_to_bytes((randrange(2,generator_384.order()))))
    menu()
```

### Biased Nonce Attack

Dado que el tamaño del nonce es menor que el orden de la curva y su tamaño es fijo, se crea un sesgo en la generación de nonces que puede ser explotada mediante un ataque con retículos. En este [video](https://www.youtube.com/watch?v=6ssTlSSIJQE) Nadia Heninger explica muy bien las mates y el funcionamiento del ataque. 

Básicamente nos dicen que podremos hallar un resultado si se cumple la siguiente restricción ( `n` es el orden de la curva y `B = 368`  es el limite superior del nonce):

$$\begin{align}
&\log{B} \leqslant \log{n(m-1)/m\ -\ (\log{m})/2 }\\
&m = \sqrt{\log{n}}
\end{align}
$$

El objetivo es crear un retículo que mediante LLL(**Lenstra–Lenstra–Lovász**) te devuelva como el vector mas corto $v_k$, un vector que contiene los nonces de cada firma. El ataque no tiene un 100% de efectividad así que puede darse el caso de que no se recupere la clave privada.

El retículo tiene la siguiente estructura:

$$
\begin{bmatrix}
n & 0 & 0 & 0 & \cdots & 0 & 0\\
0 & n & 0 & 0 & \cdots & 0 & 0\\
0 & 0 & n & 0 & \cdots & 0 & 0\\
0 & 0 & 0 & n & \cdots & 0 & 0\\
\vdots & \vdots & \vdots & \vdots & \ddots & \vdots & \vdots \\
r_1s_1^{-1} & r_2s_2^{-1} & r_3s_3^{-1} & r_4s_4^{-1} & \cdots & \frac{B}{n} & 0 \\ 
m_1s_1^{-1} & m_2s_2^{-1} & m_3s_3^{-1} & m_4s_4^{-1} & \cdots & 0 & B \\
\end{bmatrix}
$$

El cálculo de la clave privada conociendo el nonce y los valores de la firma:

$$
d = r^{-1}(ks - H(m))
$$

Tras aplicar el algoritmo `LLL` comprobamos si el primer valor en cada fila (que equivale a un vector) corresponde con el nonce de la primera firma para recuperar la clave privada. También es necesario guardar la clave pública que se utiliza para las firmas mediante ECDSA para comprobar que hemos recuperado la clave privada. El servidor devuelve la clave pública al iniciar sesión con cualquier token válido.

```python
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
```

Una vez tengamos la clave privada podremos generar nuestros propios tokens. Utilizando la librería del reto `JWS` podemos firmarlos con la función `encode` pasando por parámetro el `payload` conveniente. 

```python
def create_payload():
    payload = dict()
    payload['username'] = "HugoBond"
    payload['dfh'] = getPrime(200)
    payload['iat'] = payload['dfh'] + 1
    payload['status'] = "Rector"
    return payload
```

## Segunda Parte - Recuperar la Flag

El token debe contener 4 campos en el payload:

1. Username: No es relevante
2. Status: Rector
3. iat: Un numero primo de 200 bits
4. Dfh: Un número mayor al iat

Al iniciar sesión si cumplimos todos estos requisitos nos devolverá un número tal que:

$$
(iat)^{flag}\ mod\ (dfh)^2
$$

Binomio de Newton:

$$\begin{align}
&(x + y)^{n} = \sum_{k=0}^{n}\binom{n}{k}x^{n-k}y^{k}\\ 
&(x + 1)^{n} = 1 + xn +\binom{n}{2} x^{2} + potencias\ mayores\ de\ n\\
&l =  (x + 1)^{n} = 1 + xn\ mod\ x^2
\end{align}$$

Utilizando esta teoría, si `x` es un número primo y `n` es la flag , podemos calcular `n` como $(l-1)/x$.  Pero dado que el módulo es mucho más pequeño que el resultado $r$,  es necesario recurrir al Teorema Chino del Resto para recuperar la flag. Por lo tanto, el **payload** de nuestro token debe seguir la siguiente estructura:

`{"username": "HugoBond", "status": "Rector", "dfh": p(numero primo), "iat": p + 1}`

Como podemos ver en el código de `administration.py`  `assert flag.bit_length() > 600` la flag esta formada por más de 600 bits. 

Se necesitan al menos 4 valores distintos de $l$, con distintos módulos coprimos entre si. Hay que iniciar sesión 4 veces distintas cambiando los valores del payload y almacenándolos. Para finalmente aplicar el CRT y recuperar la flag. 

```python
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
```

### Solver Completo del Reto

```python
import json

from Crypto.Util.number import isPrime, long_to_bytes, bytes_to_long, getPrime
from pwn import process
from library import JWS
from ecdsa.ecdsa import generator_384
from hashlib import sha256
from sage.all import QQ, Matrix, crt

r = process(["python3","administration.py"]) 

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
```
