import json
import base64
import hmac

from os import urandom
from hashlib import sha512,sha256,blake2b
from Crypto.Util.number import long_to_bytes, bytes_to_long
from ecdsa.ecdsa import Public_key, Private_key, Signature,  generator_384



class JWS:
    def __init__(self,key:int):
        self.header = None
        self.payload = None
        self.ALGORITHMS = ["HSMAC256", "ES512", "ESBLK"]
        self.pubKey = Public_key(generator_384, bytes_to_long(key)*generator_384)
        self.privKey = Private_key(self.pubKey, bytes_to_long(key))
        self.key = key


    @staticmethod
    def base64url_encode(data:bytes):
        return base64.urlsafe_b64encode(data).replace(b"=", b"")
    
    @staticmethod
    def base64url_decode(data:bytes):
        res = len(data) % 4
        if res > 0:
            data += b"=" * (4 - res)
        return base64.urlsafe_b64decode(data)

    @staticmethod
    def load_token(token:str):
        header,payload,sign = token.split(".")
        header = JWS.base64url_decode(header.encode())
        payload = JWS.base64url_decode(payload.encode())
        sign = JWS.base64url_decode(sign.encode())
        return (header, payload, sign)


    def sign(self, payload, header, key:bytes, algorithm="HSMAC256"):
        sign_input = ".".join([header, payload])
        if algorithm not in self.ALGORITHMS:
            raise ValueError(f"ALgorithm {algorithm} not supported.")

        if algorithm == "HSMAC256":
            signature = hmac.new(key, sign_input.encode(), digestmod=sha256).digest()
        else:
            signature = self.ecdsa_sign(sign_input, key, algorithm)

        return signature


    def verify(self, token):
        try:
            header, payload, signature = JWS.load_token(token)
            sign_input = b".".join([header, payload]) 
            hd = json.loads(header)
            algorithm = hd['alg']
        except:
            raise Exception("ERROR: Invalid token.")

        if algorithm == "HSMAC256":
            return signature == self.sign(payload.decode(), header.decode(), self.key)

        elif algorithm == "ES512" or algorithm == "ESBLK":
            bytes_r,bytes_s = signature.split(b'&&')
            r = bytes_to_long(bytes_r)
            s = bytes_to_long(bytes_s)
            sign = Signature(r, s)
            token_hash = bytes_to_long(sha256(sign_input).digest())
            return self.pubKey.verifies(token_hash,sign)

        else:
            raise Exception(f"Algoritmo desconocido {algorithm}.")
              

    def encode(self, payload, algorithm="HSMAC256"):
        if algorithm not in self.ALGORITHMS:
            raise ValueError(f"ALgorithm {algorithm} not supported.")
        
        try:
            self.payload = json.loads(payload)      
        except:
            raise Exception("Invalid payload format.")

        if algorithm == "HSMAC256":
            self.header = '{"alg":"HSMAC256","typ":"JWT"}'
        
        elif algorithm == "ES512":
            self.header = '{"alg":"ES512","typ":"JWS"}'

        elif algorithm == "ESBLK":
            self.header = '{"alg":"ESBLK","typ":"JWS"}'

        signature = self.sign(payload,self.header, self.key, algorithm)
        token = ".".join([JWS.base64url_encode(data).decode() for data in [self.header.encode(),payload.encode(),signature]])
        return token
            
        
    def ecdsa_sign(self, input:str, key:bytes, algorithm:str):
        if algorithm == "ES512":
            hash = sha512()
        else:
            hash = blake2b(digest_size=46)
            
        hash.update(key + urandom(16))
        nonce = bytes_to_long(hash.digest())
        sign = self.privKey.sign(bytes_to_long(sha256(input.encode()).digest()), nonce)
        
        return long_to_bytes(sign.r)+ b'&&' +long_to_bytes(sign.s)

    