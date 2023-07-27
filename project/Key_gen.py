from Crypto.PublicKey import RSA
from os.path import exists
from os import getcwd
import base64
import pyasn1.codec.der.decoder
import pyasn1.codec.der.encoder
import pyasn1.type.univ
import re
from random import uniform
from constants import File_ERROR
from equations import logistic_3d
from ctypes import CDLL,c_double
from struct import pack

# gen rsa key and write it
def generate_key_rsa(ksize,Path):
    key = RSA.generate(ksize)
    Priv_key = key.exportKey('PEM')
    Pub_key = key.public_key().exportKey('PEM')
    PubFileName ,PrivFileName= '/PubKey' , '/PrivKey'
    i = 0
    while exists(Path+PubFileName+'.key') or exists(Path+PrivFileName+'.key'):
        i += 1
        if PubFileName.endswith('(%d)'%(i - 1)) or PrivFileName.endswith('(%d)'%(i - 1)):
            PrivFileName = PrivFileName[:len(PrivFileName)-3]
            PubFileName = PubFileName[:len(PubFileName)-3]
            PrivFileName = PrivFileName + '({})'.format(i)
            PubFileName = PubFileName + '({})'.format(i)
            continue
        PrivFileName = PrivFileName + '({})'.format(i)
        PubFileName = PubFileName + '({})'.format(i)

    Priv_key_File = Path + PrivFileName + '.key'
    Pub_key_File = Path + PubFileName + '.key'
    fd = open(Priv_key_File,'wb')
    fd.write(Priv_key)
    fd = open(Pub_key_File, 'wb')
    fd.write(Pub_key)
    fd.close()


def read_seq(keyfile):
    fd = open(keyfile,'rb')
    #fd.seek(32,0)
    Seq = fd.read()                  #length is 176
    x=re.findall('^(?!-----BEGIN MARCA KEY-----|-----END MARCA KEY-----).+$',Seq.decode(),re.MULTILINE)
    template = '{}\n{}'
    return template.format(x[0],x[1]).encode()

def Export_marcakey(x,y,z,lamda,beta,alfa):
    seq = pyasn1.type.univ.Sequence()
    for i,x in enumerate((x,y,z,lamda,beta,alfa)):
        seq.setComponentByPosition(i, pyasn1.type.univ.OctetString(str(x)))
    template = '-----BEGIN MARCA KEY-----\n{}-----END MARCA KEY-----\n'
    der = pyasn1.codec.der.encoder.encode(seq)
    key = base64.encodebytes(der)
    return template.format(key.decode()).encode()

def Import_marcakey(keyfile):
    try:
        seq = read_seq(keyfile)
        seq = base64.decodebytes(seq)
        key = pyasn1.codec.der.decoder.decode(seq)
        key_values = []
        for i in range(6):
            key_values.append(float(key[0][i]))
        return key_values
    except:
        return File_ERROR
def generate_init_seeds():
    x = uniform(0,1)
    while x == 0 or x == 1:
        x = uniform(0,1)
    y = uniform(0,1)
    while abs(y - x) == pow(2, -49):
        y = uniform(0, 1)
        while y == 0 or y ==1:
            y = uniform(0, 1)

    z = uniform(0,1)
    while abs(z-x) == pow(2,-49) or abs(z-y) == pow(2,-49):
        z = uniform(0,1)
        while z == 0 or z ==1:
            z = uniform(0, 1)
    x=float('{:.16f}'.format(x));y=float('{:.16f}'.format(y));z=float('{:.16f}'.format(z))
    lamda = uniform(3.53,3.81)
    while lamda == 3.53 or lamda ==3.81:
        lamda = uniform(3.53, 3.81)
    beta = uniform(0,0.022)
    while beta == 0 or beta == 0.022:
        beta = uniform(0, 0.022)
    alfa = uniform(0,0.015)
    while beta == 0 or beta == 0.015:
        alfa = uniform(0, 0.015)
    lamda=float('{:.4f}'.format(lamda));beta=float('{:.4f}'.format(beta));alfa=float('{:.4f}'.format(alfa))

    return x,y,z,lamda,beta,alfa

def generate_key_marca(key_path):
    x,y,z,a,b,c=generate_init_seeds()
    key = Export_marcakey(x,y,z,a,b,c)
    fd = open(key_path,'wb')
    fd.write(key)


def generate_init_marca_keys(seq):
    a,b,c,d,e,f = seq
    k = b'';k2 = b''; nonce = b''
    wrapper = CDLL(getcwd()+'/lib/mantissa.so')
    x,y,z = logistic_3d(a,b,c,d,e,f,100)

    k += pack('!l',wrapper.mantissa_xor(c_double(x),c_double(y),c_double(z)))
    for i in range(7):
        x, y, z = logistic_3d(x, y, z, d, e, f, 50)

        k += pack('!l', wrapper.mantissa_xor(c_double(x), c_double(y), c_double(z)))

    for i in range(4):
        x, y, z = logistic_3d(x, y, z, d, e, f, 50)

        k2 += pack('!l', wrapper.mantissa_xor(c_double(x), c_double(y), c_double(z)))

    for i in range(2):
        x, y, z = logistic_3d(x, y, z, d, e, f, 50)

        nonce += pack('!l', wrapper.mantissa_xor(c_double(x), c_double(y), c_double(z)))
    return k,k2,nonce
'''
x = Import_marcakey('fathy.mkey')
z = generate_init_marca_keys(x)
print(z)
print(len(z[0]),len(z[1]),len(z[2]))
#print(logistic_3d(x,y,z,a,b,c,100))

with open('fathy.mkey','wb') as f:
    f.write(Export_marcakey(0.9275413174568904,0.4752369852233585,0.2233654789523658,3.8,0.0019,0.015))
print(Import_marcakey('fathy.mkey'))

print(read_seq('fathy.mkey'))
'''