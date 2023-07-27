from Crypto.Cipher import AES
from File_enc import File_KDF
from struct import unpack
class CipherAes():
    def __init__(self,Key : bytes ,IV : bytes ):
        self.IV = IV
        self.Key = Key

    def BlockCipher(self):
        Block_Crypter = AES.new(self.Key,AES.MODE_CBC,self.IV[:16])
        return Block_Crypter

class File_KDF_AES(File_KDF):
    def __init__(self,File : str ,headers : list, oper : bool):
        super(File_KDF_AES, self).__init__(File,headers , oper)
        self.block_size = 16
        self.__Prepare_Cipher()

    def __Prepare_Cipher(self):

        self.k1,self.iv,self.ksize,self.fsize = self.headers[0],self.headers[1],self.headers[2],self.headers[3]
        self.BlockCipher = CipherAes(self.k1,self.iv).BlockCipher()

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