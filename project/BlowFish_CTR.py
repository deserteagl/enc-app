from Crypto.Cipher import Blowfish
from File_enc import File_KDF
from struct import unpack
"""key = b'\xbe\xa5\xde\xe2t\x9e\xeeS\xa9nh!\x11\x06\xb0\x90<\xbc\xfc\xcd\xac\xd3\xa8 \xacE\x04\x9e\x91\xbfP\xf6'
data = b'1234'
cipher = Blowfish.new(key,Blowfish.MODE_CTR,nonce=b'1234567')

print(key)
print(cipher.nonce)
c = cipher.decrypt(b'\x04\xfb\xb7\xdd')
print(c)
"""
#key 32 nonce 7
class CipherBlowFish():
    def __init__(self,IV : bytes ,Key : bytes ):
        self.IV = IV
        self.Key = Key

    def BlockCipher(self):
        Block_Crypter = Blowfish.new(self.Key,Blowfish.MODE_CBC,self.IV[:8])
        return Block_Crypter

class File_KDF_BlowFish(File_KDF):
    def __init__(self,File : str ,headers : list, oper : bool):
        super(File_KDF_BlowFish, self).__init__(File,headers , oper)
        self.block_size = 8
        self.__Prepare_Cipher()

    def __Prepare_Cipher(self):
        self.k1,self.iv,self.ksize,self.fsize = self.headers[0],self.headers[1],self.headers[2],self.headers[3]
        self.BlockCipher = CipherBlowFish(self.iv,self.k1).BlockCipher()

    def decrypt(self):
        chunksize = 24 * 1024
        self.ifd.seek(self.ksize, 0)
        size = self.fsize
        fsize = unpack('!Q', size)[0]
        while True:
            chunk = self.ifd.read(chunksize)
            if len(chunk) == 0:
                break
            self.ofd.write(self.BlockCipher.decrypt(chunk))
        self.ofd.truncate(fsize)
        del chunk ; del chunksize
        self.ofd.close()
        self.ifd.close()