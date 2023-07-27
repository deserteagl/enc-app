from ctypes import CDLL,create_string_buffer,c_void_p,c_size_t
from constants import NotBytesError,File_ERROR,IO_ERROR
from File_enc import File_KDF
from os.path import splitext
from struct import unpack
from threading import Lock
from time import sleep
lock = Lock()
class new:
    def __init__(self,k1,k2,nonce):

        block_cipher = CDLL('./lib/Marca.so')
        block_cipher.prep.argtype = c_void_p
        block_cipher.prep(k1,k2,nonce)
        self.block_cipher=block_cipher

    def encrypt(self,data,counter):
        data_len = len(data)
        pt = create_string_buffer(data,data_len)
        ct = create_string_buffer(data_len)
        counter = self.block_cipher.MarcaCipher(pt,ct,data_len,counter)

        return ct.raw,counter

    def decrypt(self, data,counter):
        data_len = len(data)
        ct = create_string_buffer(data, data_len)
        pt = create_string_buffer(data_len)
        counter = self.block_cipher.MarcaDecipher(ct, pt, data_len,counter)
        return pt.raw,counter

    def stop_operations(self):
        self.block_cipher.block.counter = 0

class CipherMarca():
    def __init__(self,k1 : bytes ,k2 : bytes ,nonce:bytes):
        self.k1 = k1
        self.K2= k2
        self.nonce = nonce

    def BlockCipher(self):
        Block_Crypter = new(self.k1,self.K2,self.nonce)
        return Block_Crypter

class File_Marca(File_KDF):
    def __init__(self,File : str ,headers : list, oper : bool,algo = 'MARCA'):
        super(File_Marca, self).__init__(File,headers , oper,algo)
        self.block_size = 16
        self.__Prepare_Cipher()


    def __Prepare_Cipher(self):
        self.k1,self.k2,self.nonce,self.ksize,self.fsize = self.headers[0],self.headers[1],self.headers[2],self.headers[3],self.headers[4]
        self.BlockCipher = CipherMarca(self.k1,self.k2,self.nonce).BlockCipher()
    def encrypt(self):
        chunksize = 64 * 1024

        self.ofd.write(self.c_headers)
        counter = 0
        while True:
            chunk = self.ifd.read(chunksize)
            if len(chunk) == 0:
                break
            elif len(chunk) % self.block_size != 0:
                chunk += b' ' * (self.block_size - len(chunk) % self.block_size)
            ct,counter = self.BlockCipher.encrypt(chunk,counter)
            self.ofd.write(ct)
        del ct ;del chunk
        self.ofd.close()
        self.ifd.close()
        self.BlockCipher.stop_operations()
    def decrypt(self):
            chunksize = 24 * 1024
            self.ifd.seek(64,0)
            size = self.ifd.read(8)
            fsize = unpack('!Q',size)[0]
            counter = 0
            while True:
                chunk = self.ifd.read(chunksize)
                if len(chunk) == 0:
                    break
                pt, counter = self.BlockCipher.decrypt(chunk,counter)
                self.ofd.write(pt)
            self.ofd.truncate(fsize)
            del pt ; del chunksize
            self.ofd.close()
            self.ifd.close()
            self.BlockCipher.stop_operations()