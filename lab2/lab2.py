import random
import json

def gcd(a, b):
    '''求最大公因数
    '''
    if b==0:
        return a
    while a%b!=0:
        r = a%b
        a, b = b, r
    return b

def fraction_add(a1, b1, a2, b2):
    '''两分数相加，返回最简化后的分数
    '''
    # a1/b1 + a2/b2
    a = a1*b2 + a2*b1
    b = b1*b2
    g = gcd(a, b)
    return a//g, b//g

def generate_key(parameter_boundary):
    k = random.randint(-parameter_boundary, parameter_boundary)
    return k

def generate_polynomial(shadow_size, key, parameter_boundary):
    '''生成t-1次多项式系数
    '''
    #y(x) = at-1*x^(t-1) + at-2*x^(t-2) + ... + a2*x^2 + a1*x + a0
    #a0==key
    l = []
    for _ in range(shadow_size - 1):
        l.append(random.randint(-parameter_boundary, parameter_boundary))
    l.append(key)
    return l

def generate_shadow_keys(polynomial, N, parameter_boundary):
    '''取n个多项式上不同的点
    '''
    #x_list:x1, x2, x3, ..., xn-1, xn
    #y_list:y1, y2, y3, ..., yn-1, yn
    x_list = []
    y_list = []
    #different x (the function of random.sample)
    x_list = random.sample(range(1, parameter_boundary), N)
    for x in x_list:
        # use 秦九韶's algorithm to caculate polynomial
        y = polynomial[0]
        for coef in polynomial[1:]:
            y = y*x +coef
        y_list.append(y)
    return x_list, y_list

#Lagrangian interpolation
def recover_key(shadow_keys, shadow_values):
    length = len(shadow_keys)
    key_a, key_b = 0, 1
    for i in range(length):
        a, b = shadow_values[i], 1
        for j in range(length):
            if j!=i:
                a, b =-shadow_keys[j]*a, (shadow_keys[i]-shadow_keys[j])*b
                g = gcd(a, b)
                a, b = a//g, b//g
        key_a, key_b = fraction_add(key_a, key_b, a, b)
    return key_a//key_b

if __name__ == "__main__":
    parameter_boundary = 2**31

    menu = '''
    Menu:
    1) generate key
    2) generate shadow keys
    3) recover the key
    4) verify the key
    5) quit
    '''

    print(menu)
    while 1:
        cmd = input('~$')
        if cmd=='1':
            key = generate_key(parameter_boundary)
            with open('key.txt', 'w') as fp:
                json.dump(key, fp)
            print('Save the key to key.txt')
        elif cmd=='2':
            with open('key.txt', 'r') as fp:
                key = json.load(fp)
            shadow_size = int(input('Please input the number of t(shadow keys):'))
            N = int(input('Please input the n:'))
            polynomial = generate_polynomial(shadow_size, key, parameter_boundary)
            with open('polynomial.txt', 'w') as fp:
                json.dump(polynomial, fp)
            shadow_keys, shadow_values = generate_shadow_keys(polynomial, N, parameter_boundary)
            with open('shadow_values.txt', 'w') as fp:
                json.dump(shadow_values, fp)
            with open('shadow_keys.txt', 'w') as fp:
                json.dump(shadow_keys, fp)
            print('The shadow keys are generated.')
        elif cmd=='3':
            with open('shadow_keys.txt', 'r') as fp:
                shadow_keys = json.load(fp)
            with open('shadow_values.txt', 'r') as fp:
                shadow_values = json.load(fp)
            with open('polynomial.txt', 'r') as fp:
                polynomial = json.load(fp)
            shadow_size = len(polynomial) # t
            samp_shadow_keys = shadow_keys[:shadow_size]
            samp_shadow_values = shadow_values[:shadow_size]

            rkey = recover_key(samp_shadow_keys, samp_shadow_values)
            with open('recover_key.txt', 'w') as fp:
                json.dump(rkey, fp)
            print('The key is recovered.')
        elif cmd=='4':
            with open('key.txt', 'r') as fp:
                key = json.load(fp)
            with open('recover_key.txt', 'r') as fp:
                rkey = json.load(fp)
            if rkey==key:
                print('Succeed.')
            else:
                print('Recover failure.')
        else:
            exit(0)