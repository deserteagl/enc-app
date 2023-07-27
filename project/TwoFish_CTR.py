from twofish import Twofish
from struct import pack
from File_enc import File_KDF
class CipherTwoFish():
    def __init__(self,key,nonce,counter=0):
        self.key = key
        self.nonce = nonce
        self.counter = counter
        self.Block_Crypter = Twofish(self.key)

    def XorWithBytes(self,a,b):
        e=([i^v for i,v in zip(a,b)])
        return bytes(e)

    def concat(self,a,b):
        e = a+b
        print(e)
        return e

    def encrypt(self,pt):
            init = self.concat(pack('>Q',self.counter),self.nonce)
            cipher = self.Block_Crypter.encrypt(init)
            ct = self.XorWithBytes(cipher,pt)
            self.counter += 1
            return ct

    def decrypt(self,ct):
            init = self.concat(pack('>Q',self.counter), self.nonce)
            cipher = self.Block_Crypter.encrypt(init)
            pt = self.XorWithBytes(ct, cipher)
            self.counter += 1
            return pt

class File_KDF_TwoFish(File_KDF):
    def __Prepare_Cipher(self):
        self.BlockCipher = CipherTwoFish(self.k2,self.k1)

