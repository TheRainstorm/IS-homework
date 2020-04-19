import random
import json

def generate_key(parameter_boundary):
    k = random.randint(-parameter_boundary, parameter_boundary)
    return k

def generate_polynomial(shadow_size, key, parameter_boundary):
    #y(x) = an-1*x^(n-1) + an-2*x^(n-2) + ... + a2*x^2 + a1*x + a0
    l = []
    for _ in range(shadow_size - 1):
        l.append(random.randint(-parameter_boundary, parameter_boundary))
    l.append(key)
    return l

def generate_shadow_keys(polynomial, parameter_boundary):
    #l1:x1, x2, x3, ..., xn-1, xn
    #l2:y1, y2, y3, ..., yn-1, yn
    l1 = []
    l2 = []
    length = len(polynomial)
    #different x (the function of random.sample)
    l1 = random.sample(range(1, parameter_boundary), length)
    for i in range(length):
        y = 0
        for j in range(length):
            y = y + ((l1[i] ** (length - j - 1)) * polynomial[j])
        l2.append(y)
    return l1, l2

#Lagrangian interpolation
def recover_key(shadow_keys, shadow_values):
    key = 0
    length = len(shadow_keys)
    for i in range(length):
        mul = 1
        for j in range(length):
            if i != j:
                mul = mul * (shadow_keys[j] / (shadow_keys[j] - shadow_keys[i]))
            else:
                mul = mul
        mul = mul * shadow_values[i]
        key = key + mul
    return key

if __name__ == "__main__":
    parameter_boundary = 2**7

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
            with open('key.txt', 'rb') as fp:
                key = json.load(fp)
            shadow_size = int(input('Please input the number of shadow keys:'))
            polynomial = generate_polynomial(shadow_size, key, parameter_boundary)
            with open('polynomial.txt', 'w') as fp:
                json.dump(polynomial, fp)
            shadow_keys, shadow_values = generate_shadow_keys(polynomial, parameter_boundary)
            with open('shadow_values.txt', 'w') as fp:
                json.dump(shadow_values, fp)
            with open('shadow_keys.txt', 'w') as fp:
                json.dump(shadow_keys, fp)
            print('The shadow keys are generated.')
        elif cmd=='3':
            shadow_keys = []
            shadow_values = []
            with open('shadow_keys.txt', 'rb') as fp:
                shadow_keys = json.load(fp)
            with open('shadow_values.txt', 'rb') as fp:
                shadow_values = json.load(fp)
            rkey = recover_key(shadow_keys, shadow_values)
            with open('recover_key.txt', 'w') as fp:
                json.dump(rkey, fp)
            print('The key is recovered.')
        elif cmd=='4':
            with open('key.txt', 'rb') as fp:
                key = json.load(fp)
            with open('recover_key.txt', 'rb') as fp:
                rkey = json.load(fp)
            if key < 0:
                if(rkey > 1.05*key and rkey < 0.95*key):
                    print('Succeed.')
                else:
                    print('Recover failure.')
            else:
                if(rkey <1.05*key and rkey > 0.95*key):
                    print('Succeed.')
                else:
                    print('Recover failure.')
        else:
            exit(0)