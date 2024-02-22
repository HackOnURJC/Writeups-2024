import os
import json

from random import randrange
from Crypto.Util.number import isPrime, long_to_bytes, bytes_to_long
from ecdsa.ecdsa import generator_384
from library import JWS

FLAG = os.environ['FLAG']

def register(username: str, algorithm: str):
    payload = dict()
    payload['username'] = username
    payload['iat'] = os.urandom(32).hex()
    payload['status'] = "Student"
    payload['dfh'] = "3+3=2 right?"
    token = jws.encode(json.dumps(payload), algorithm)
    print(token)


def login(token: str):
    if jws.verify(token):
        try:
            _,payload,_ = JWS.load_token(token)
            payload = json.loads(payload)
            status = payload['status']
            username = payload['username']
            iat = payload['iat']
            dfh = payload['dfh']
        except:
            print("Problem in your payload detected.")
            exit()

        if status == "Rector" and type(dfh) == int == type(iat):
            flag = bytes_to_long(FLAG.encode())
            assert flag.bit_length() > 600
            if iat > dfh and dfh.bit_length() == 200 and isPrime(dfh):
                print(f"Rector, this belongs to you: {pow(iat,flag,dfh**2)}")
            else:
                print("Bad Parameters.")
        else:
            print(f"Welcome {username},your iat is {iat} and your status is {status}")   
            print(f"This is your public key: ")
            print(jws.pubKey.point.x(),jws.pubKey.point.y()) 
    else:
        print("Fail in Log In. Invalid Token.")


def show_options():
    print("\n1. Log In - With token.\n2. Register.\n3. Make a complain.\n4. Exit\n")


def banner():
    print(
        """
    __  __           __   ____      
   / / / /___ ______/ /__/ __ \____ 
  / /_/ / __ `/ ___/ //_/ / / / __ \\
 / __  / /_/ / /__/ ,< / /_/ / / / /
/_/ /_/\__,_/\___/_/|_|\____/_/ /_/ 
Welcome to the HackOn administration."""
        )


def menu():
    banner()
    show_options()
    for i in range(34):
        try:
            option = int(input("[*]Option: ").strip())
        except:
            print("Wait, what?")
            exit()
            
        if option == 1:
            token = input("Token, please: ").strip()
            login(token)
            
        elif option == 2:
            new_user = input("Username: ").strip()
            algorithm = input("Alg: ").strip()
            register(new_user, algorithm)

        elif option == 3:
            print("Fuck no, send bizum to this number +34 631223245 to get the flag")

        else:
            print("Goodbye!!")
            exit()


if __name__ == '__main__':
    jws = JWS(long_to_bytes((randrange(2,generator_384.order()))))
    menu()

