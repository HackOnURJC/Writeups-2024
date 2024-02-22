import hashlib

def buildTree(word):
    message = 'The password that I use is the same as in the Google account it is ' + word
    message = message.split(' ')
    leaves1 = [hashlib.sha256(word.encode()).hexdigest() for word in message]
    i = 0

    while len(leaves1) > 1:
        leaves2 = []
        i = 0
        while(i < len(leaves1)):
            aux = leaves1[i]
            if i + 1 < len(leaves1):
                aux += leaves1[i+1]
            leaves2.append(hashlib.sha256(aux.encode()).hexdigest())
            i += 2
        leaves1 = leaves2
    return leaves1[0]

originalRoot = '30c085686aa4b1d76ac1c72dfefab6f4a02f5e3865acd76f868b6d5781d2efc8'

with open("rockyou.txt") as file:
    for line in file:
        newRoot = buildTree(line.strip())
        print("Trying password ", line)
        if(originalRoot == newRoot):
            print("The password is:", line)
            break