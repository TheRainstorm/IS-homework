import random

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
    # sender's private r
    r = random.randint(1, g_p)

    ciphertext = []
    for ch in message:
        A = plus(g_coding_table[ord(ch)], mul_k(public_key[1], r))
        B = mul_k(public_key[0], r)
        ciphertext.append((A, B))
    return ciphertext

def decrypt(ciphertext, private_key):
    message = ''
    for e in ciphertext:
        A, B = e
        M = plus(A, neg(mul_k(B, private_key)))
        ch = chr(g_coding_table.index(M))

        message += ch
    return message

if __name__ == "__main__":
    #1 domain parameter
    g_a, g_b, g_p = 1, 1, 2**107-1
    
    # verify
    if (4*g_a**3 + 27*g_b**2)%g_p==0:
        print("(4*a**3 + 27*b**2)%p==0")
        exit(0)
    
    #2 gen-key
    public_key, private_key = generate_key()
    print("keys:\n",public_key, private_key)

    #3 coding
    g_coding_table = generate_coding_table()
    #4 send
    message = 'hello world'
    ciphertext = encrypt(message, public_key)
    print("\nciphertext:\n,",ciphertext)
    #5 reciever
    message = decrypt(ciphertext, private_key)
    print("\nmessage:\n",message)


