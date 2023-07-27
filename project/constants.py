from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from struct import pack
KDF = b'#KDF'
OEAP = b'#SGN'
aes = pack('!I',0x01)
blowfish = pack('!I',0x02)
algorithms = {'AES' : aes,'TWOFISH' : blowfish,'BLOWFISH' : blowfish}

SUCCESS = 0
File_ERROR = 1
IO_ERROR = 2
VERIFY_FALSE = 3
PASS_Valid = 4
PASS_Invalid = 5
Not_Private_key = 6
KeyFile_error = 7
NotBytesError = 8
# 1024 is \xFF\x03 , 2048 is \xFF\x07 , 4096 is \xFF\x0F
'''
pt = b'1233'
k = RSA.generate(1024)
pk = k.public_key()
cipher = PKCS1_OAEP.new(k)
ct = cipher.encrypt(b'1234')
#print(ct)
tk = RSA.generate(1024)
print(tk.p,'\n',tk.q)
#ci = PKCS1_OAEP.new(tk)
#pt = ci.decrypt(ct)
'''

