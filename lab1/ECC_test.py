import random
import json
import sys
import threading as td
import time

def gcd_and_xy(a, b):
    '''use Euclid Algorithm to cacluate:
        1. gcd(a, b)
        2. ax + by = gcd(a, b), the one of (x, y)
    '''
    x1, y1 = 1, 0
    x2, y2 = 0, 1

    while a%b!=0:
        q, r = a//b, a%b
        x3, y3 = x1 - q*x2, y1 - q*y2

        a, b = b, r     # shift right
        x1, x2 = x2, x3
        y1, y2 = y2, y3
    return r, (x3, y3)

def ni(x):
    '''
    get the x^-1 mod p
    '''
    # for e in range(1, g_p-1):
    #     if (x*e)%g_p == 1:
    #         return e
    return gcd_and_xy(x, g_p)[1][0]

def infinity(): # infinity point
    return (-1, -1)

def is_infinity(p): 
    if p[0]==-1 and p[1]==-1:
        return True
    return False

def plus(p1, p2): # P1 + P2
    '''
    The addition on Ellipitic Curve
    '''
    x1, y1 = p1
    x2, y2 = p2
    if is_infinity(p1):
        return p2
    elif is_infinity(p2):
        return p1
    elif x1==x2 and y1==y2:
        k =(3*x1**2+g_a)*ni(2*y1)%g_p
    elif x1==x2:
        return infinity()
    else:
        k = ((y2 - y1) * ni(x2 - x1))%g_p
    
    x3 = (k**2 - x1 - x2) %g_p
    y3 = (k*(x1 - x3) - y1) %g_p

    return (x3, y3)

def neg(p): # -P
    return (p[0], -p[1])

def mul_2(p):
    return plus(p, p)

def mul_k(p, k):
    if k==1:
        return p
    
    if k%2==1:
        pp = mul_k(p, (k-1)//2)
        return plus(plus(pp, pp), p)
    else:
        pp = mul_k(p, k//2)
        return plus(pp, pp)

def print_all_points():
    p0 = (0, 1)
    p = (0, 1)
    for i in range(g_p+1):
        p = plus(p0, p)
        print("{:3d}P0:\t".format(i+2), p)
        if is_infinity(p):
            break
    print('all points:')
    cnt = 0
    for i in range(g_p):
        for j in range(g_p):
            if (j**2 - i**3 - i - 1) %g_p ==0:
                cnt += 1
                print("{:3d}:\t".format(cnt), (i, j))

def generate_key():
    '''
    private_key: k
    public_key: (P, kP)
    '''
    k = random.randint(1, g_p)
    P = (0, 1)
    G = mul_k(P, k)
    return (P, G), k

def generate_coding_table():
    coding_table = []
    p0 = (0, 1)
    p = (0, 1)
    coding_table.append(p0)
    for i in range(1, 2**8):
        p = plus(p0, p)
        if is_infinity(p):
            print("Prime p needs to be bigger")
            exit(0)
        coding_table.append(p)
    return coding_table

def encrypt(message, public_key):
    '''
    message: byte array
    '''
    global ciphertext
    # sender's private r
    r = random.randint(1, g_p)

    for byt in message:
        try:
            A = plus(g_coding_table[byt], mul_k(public_key[1], r))
            B = mul_k(public_key[0], r)
            ciphertext.append((A, B))
        except:
            print(byt)

def decrypt(ciphertext, private_key):
    global message
    for e in ciphertext:
        A, B = e
        M = plus(A, neg(mul_k(B, private_key)))
        byt = g_coding_table.index(M).to_bytes(1, 'little')

        message += byt
    return message

if __name__ == "__main__":
    #1 domain parameter
    g_a, g_b, g_p = 1, 1, 2**107-1
    # verify
    if (4*g_a**3 + 27*g_b**2)%g_p==0:
        print("(4*a**3 + 27*b**2)%p==0")
        exit(0)
    #3 byte to point
    g_coding_table = generate_coding_table()

    menu = '''
    Menu:
    1) generate keys
    2) send message use specific public key (EOF line to finish)
    3) decode message use specific private key
    4) quit
    '''
    print(menu)
    while 1:
        cmd = input('~$')
        if cmd=='1':
            print('Use the default Ep(a, b) parameter:\n', g_a, g_b, g_p)
            #2 gen-key
            public_key, private_key = generate_key()
            with open('id_ecc.pub', 'w') as fp:
                json.dump(public_key, fp)
            with open('id_ecc', 'w') as fp:
                json.dump(private_key, fp)
            print('Save to id_ecc.pub(public key) & id_ecc(private key)')
        elif cmd=='2':
            #4 send
            lines = sys.stdin.readlines()
            message = ''.join(lines).encode('utf-8')

            with open('id_ecc.pub', 'rb') as fp:
                public_key = json.load(fp)

            ciphertext = []
            thread1 = td.Thread(name='encrypt', target=encrypt, args=(message, public_key))
            thread1.start()
            cnt = 0
            while thread1.is_alive():
                sys.stdout.write("\rencrypting...%d"%(cnt))
                sys.stdout.flush()
                time.sleep(1)
                cnt += 1
            sys.stdout.write("\r                    \r")
            
            with open('ciphertext.json', 'w') as fp:
                json.dump(ciphertext, fp)
        elif cmd=='3':
            #5 reciever
            with open('id_ecc', 'rb') as fp:
                private_key = json.load(fp)
            with open('ciphertext.json', 'rb') as fp:
                ciphertext = json.load(fp)
            
            message = b''
            thread2 = td.Thread(name='decrypt', target=decrypt, args=(ciphertext, private_key))
            thread2.start()
            cnt = 0
            while thread2.is_alive():
                sys.stdout.write("\rdecrypting...%d"%(cnt))
                sys.stdout.flush()
                time.sleep(1)
                cnt += 1
            sys.stdout.write("\r                    \r")

            print(message.decode('utf-8'))
            print('bytes:\n', message)
        else:
            exit(0)