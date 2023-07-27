'''
equations
3d logistic->
xn+1=λ∗xn∗(1−xn) +β∗y2n∗xn+α∗z3n
yn+1=λ∗yn∗(1−yn) +β∗z2n∗yn+α∗x3n
zn+1=λ∗zn∗(1−zn) +β∗x2n∗zn+α∗y3n(3)
'''

def generate_Nv_3d(x,y,z,l,b,a):
    x = (l*x*(1-x)+(b*pow(y,2)*x)+(a*pow(z,3)))
    return x

def logistic_3d(x,y,z,l,b,a,ran):
    nv_1 = x;nv_2 =y;nv_3 = z
    for i in range(ran+1):
        nv_1 = generate_Nv_3d(nv_1,y,z,l,b,a)
        nv_2 = generate_Nv_3d(nv_2,z,x,l,b,a)
        nv_3 = generate_Nv_3d(nv_3,x,y,l,b,a)

    return nv_1,nv_2,nv_3
























'''

from math import floor,trunc,gcd,pi,sin
from sympy import isprime

def logistic_skey(x,y,ran):
    for i in range(ran):
        x = generate_Nv_skew(x,y)
    return x

'''
                 #[p,q,N,e,d]
'''
def second_stage(x,y,rows):            #m is rows count
    row = []
    x = logistic_skey(x,y,100)
    for i in range(rows):
        x = logistic_skey(x,y,1)
        f = x - floor(x)
        n = trunc(f*pow(10,8))
        n = n % rows
        row.append(n)
    return row

def third_stage(y,r,columns):       #n is columns count
    cols = []
    y = logistic_sin(y,r,columns)
    for i in range(columns):
        y = logistic_sin(y,r,1)
        f = y -floor(y)
        n = trunc(f*pow(10,8))
        n = n % columns
        cols.append(n)
    return cols
skew tent->
xn+1 = xn /y        if xn<y
xn+1 = 1-xn/1-y     if xn>y

sin map->
yn+1 = r*sin(bi*yn)
'''
#print(first_stage(0.9275413174568904,0.4752369852233585,0.2233654789523658,3.8,0.0019,0.015))
#print(((230**461)%225481)%255)
#print(modinv(38,((38**143681)%225481))/230)
'''n = 487* 463
x=(3**461)%n
print(x)
s = (x**143681)%n
print(s)'''


'''
def find_complement(barr):
    c = bytearray(barr)
    for i in range(len(barr)):
        c[i] = ~barr[i]&0xFF
    return c
def gray(barr):
    c = bytearray(barr)
    for i in range(len(barr)):
        c[i] = barr[i]^(barr[i]>>1)
    return c
def gtob(barr):
    c = bytearray(barr)
    for i in range(len(barr)):
        c[i] = a[barr[i]]
    return c

b = bytearray([0x07])
a=[0, 1, 3, 2, 7, 6, 4, 5, 15, 14, 12, 13, 8, 9, 11, 10, 31, 30, 28, 29, 24, 25, 27, 26, 16, 17, 19, 18, 23, 22, 20, 21, 63, 62, 60, 61, 56, 57, 59, 58, 48, 49, 51, 50, 55, 54, 52, 53, 32, 33, 35, 34, 39, 38, 36, 37, 47, 46, 44, 45, 40, 41, 43, 42, 127, 126, 124, 125, 120, 121, 123, 122, 112, 113, 115, 114, 119, 118, 116, 117, 96, 97, 99, 98, 103, 102, 100, 101, 111, 110, 108, 109, 104, 105, 107, 106, 64, 65, 67, 66, 71, 70, 68, 69, 79, 78, 76, 77, 72, 73, 75, 74, 95, 94, 92, 93, 88, 89, 91, 90, 80, 81, 83, 82, 87, 86, 84, 85, 255, 254, 252, 253, 248, 249, 251, 250, 240, 241, 243, 242, 247, 246, 244, 245, 224, 225, 227, 226, 231, 230, 228, 229, 239, 238, 236, 237, 232, 233, 235, 234, 192, 193, 195, 194, 199, 198, 196, 197, 207, 206, 204, 205, 200, 201, 203, 202, 223, 222, 220, 221, 216, 217, 219, 218, 208, 209, 211, 210, 215, 214, 212, 213, 128, 129, 131, 130, 135, 134, 132, 133, 143, 142, 140, 141, 136, 137, 139, 138, 159, 158, 156, 157, 152, 153, 155, 154, 144, 145, 147, 146, 151, 150, 148, 149, 191, 190, 188, 189, 184, 185, 187, 186, 176, 177, 179, 178, 183, 182, 180, 181, 160, 161, 163, 162, 167, 166, 164, 165, 175, 174, 172, 173, 168, 169, 171, 170]
print(b)
c = find_complement(b)
print(c)
x=gray(b)
print(gray(b)[0])
print(gtob(x)[0])



'''

'''def generate_Nv_skew(x,y):
    if x<=y:
        x = x/y
    elif x>y:
        x = (1-x)/(1-y)
    return x

def generate_Nv_sin(y,r):
    y = r*sin(180*y)
    print(y)
    return y

def logistic_sin(y,r,ran):
    for i in range(ran):
        y = generate_Nv_sin(y,r)
    return y

def check_e(p,q,e):
    segma = (p-1)*(q-1)
    if gcd(e,segma) == 1:
            return True
    return False

def trunc_floor(n):
    f = n - floor(n)
    n = trunc(f*pow(10,3))
    return n

def egcd( a, b):
        if a == 0:
            return (b, 0, 1)
        else:
            g, y, x = egcd(b % a, a)
            return (g, x - (b // a) * y, y)

def modinv( a, m):
        g, x, y = egcd(a, m)
        if g != 1:
            raise Exception('modular inverse does not exist')
        else:
            return x % m

def first_stage(x,y,z,l,b,a):
    n1,n2,n3 = logistic_3d(x,y,z,l,b,a,101)
    n1,n2,n3 = trunc_floor(n1),trunc_floor(n2),trunc_floor(n3)
    while not check_e(n1,n2,n3) & isprime(n1) &  isprime(n2):
        n1,n2,n3 = logistic_3d(n1, n2, n3, l, b, a,1)
        n1, n2, n3 = trunc_floor(n1), trunc_floor(n2), trunc_floor(n3)
    phi = (n1-1)*(n2-1)
    d=modinv(n3,phi)
    return n1,n2,n1*n2,n3,d    
'''
