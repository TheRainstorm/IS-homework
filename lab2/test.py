import numpy as np

np.set_printoptions(suppress=True)

#y(x) = an-1*x^(n-1) + an-2*x^(n-2) + ... + a2*x^2 + a1*x + a0
# coefficient_list =  [-18, 10, -52, 79, -62]
# x_list =            [106, 125, 48, 103, 7]
# y_list =            [-2261124328, -4375802687, -94561646, -2015532181, -41845]
# coefficient_list =    [-11, -25, -103, -61, -48, -62]
# x_list =              [11, 77, 4, 103, 31, 82]
# y_list =              [-2282650, -30700840078, -25486, -130447123234, -341137330, -41968892218]
# coefficient_list =  [-27, 116, 105, 121, -21, -101, -14, -62]
# x_list =            [53, 106, 36, 113, 119, 88, 80, 52]
# y_list =            [-29101273020599, -3893833095574998, -1856774608838, -6108574139830619, -8792209469678249, -1048991876399694, -535473327239582, -25423742344998]
# coefficient_list =  [-11, -110, 84, -22, 17, 68, -109, -62]
# x_list =            [91, 100, 25, 17, 3, 19, 89, 37]
# y_list =            [-630380047300975, -1209162182330962, -93182116537, -7051326209, -84935, -14802371767, -540744932678777, -1320695942509]

# coefficient_list =  [128, -120, 116, 4, -101, 72, -49, -72, -72, -62]
# x_list =            [103, 102, 86, 108, 22, 20, 41, 10, 15, 54]
# y_list =            [165505113582708815352, 151579185677466631354, 32582885013147162874, 253671361251755778082, 148234649879034, 62612423897698, 40969295569596964, 117154563018, 4632995140408, 491230290148038010]
coefficient_list =  [90, 3, 33, -55, 62]
x_list =            [73, 7, 89, 85, 77]
y_list =            [2557180645, 218413, 5649173157, 4700132437, 3165334773]
def polynomial(x):
    # y = 0
    # for i, coef in enumerate(coefficient_list):
    #     y += coef*x**(N-1-i)
    # return y
    y = coefficient_list[0]
    for coef in coefficient_list[1:]:
        y = y*x +coef
    return y

y2_list = list(map(polynomial, x_list))

print(y_list== y2_list)

# N = len(coefficient_list)
# M = np.zeros((N, N+1), dtype=np.int64)
# '''
# [x1^t-1, x1^t-2, ..., 1, y_{i1}]
# [x2^t-1, x2^t-2, ..., 1, y_{i2}]
# :
# .
# [xt^t-1, xt^t-2, ..., 1, y_{it}]
# '''
# for i in range(N): 
#     for j in range(N):
#         M[i][j] = x_list[i]**(N-1-j)
# for i in range(N):
#     M[i][N] = y_list[i]

# print(M)
# print(np.linalg.matrix_rank(M))

def gcd(a, b):
    if b==0:
        return a
    while a%b!=0:
        r = a%b
        a, b = b, r
    return b

def fraction_add(a1, b1, a2, b2):
    # a1/b1 + a2/b2
    a = a1*b2 + a2*b1
    b = b1*b2
    g = gcd(a, b)
    return a//g, b//g

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

rkey = recover_key(x_list, y_list)
print(rkey, coefficient_list[-1])