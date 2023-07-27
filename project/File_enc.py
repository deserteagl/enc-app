from os import stat
from os.path import splitext,exists
from constants import File_ERROR,IO_ERROR,SUCCESS
from struct import pack
from PyQt5.QtCore import QThread,pyqtSignal
from time import sleep
def inverse(k):
    key = b''
    for i in range(len(k)//2):
        key += (chr(k[i])+chr(k[len(k)-i-1])).encode()
    return key[:len(key)//2],key[len(key)//2:]

def permutation(key):
    k = inverse(key)
    return k

class File_KDF(QThread):
    def __init__(self,File : str ,headers : list, oper : bool,algo:str = None):
        super(File_KDF, self).__init__()
        self.oper = oper                                     # 1 if enc 0 if dec
        self.headers = headers[1]
        self.c_headers = headers[0]
        self.block_size = 0
        if algo == 'MARCA':
            if self.oper == 1:
                i = 0
                out_file = splitext(File)[0]
                while exists(out_file + '.mfai'):
                    i += 1
                    if out_file.endswith('(%d)' % (i-1)):
                        out_file = out_file[:len(out_file) - 3]
                        out_file = out_file + '({})'.format(i)
                        continue
                    out_file  = out_file + '({})'.format(i)
                out_file = out_file + '.mfai'
            else:
                i = 0
                out_file = splitext(File)[0]
                while exists(out_file):
                    i += 1
                    if out_file.endswith('(%d)' % (i-1)):
                        out_file = out_file[:len(out_file) - 3]
                        out_file = out_file + '({})'.format(i)
                        continue
                    out_file  = out_file + '({})'.format(i)


            try:
                self.ifd = open(File, 'rb')
                self.ofd = open(out_file, 'wb')
            except FileNotFoundError:
                return File_ERROR
            except IOError:
                return IO_ERROR
        else:
            if self.oper == 1:
                i = 0
                out_file = splitext(File)[0]
                while exists(out_file + '.fai'):
                    i += 1
                    if out_file.endswith('(%d)' % (i-1)):
                        out_file = out_file[:len(out_file) - 3]
                        out_file = out_file + '({})'.format(i)
                        continue
                    out_file  = out_file + '({})'.format(i)

                out_file = out_file + '.fai'
            else:
                i = 0
                out_file = splitext(File)[0]
                while exists(out_file):
                    i += 1
                    if out_file.endswith('(%d)' % (i-1)):
                        out_file = out_file[:len(out_file) - 3]
                        out_file = out_file + '({})'.format(i)
                        continue
                    out_file = out_file + '({})'.format(i)

            try:
                self.ifd = open(File, 'rb')
                self.ofd = open(splitext(File)[0] + '.fai', 'wb') if self.oper == 1 else open(splitext(File)[0], 'wb')
            except FileNotFoundError:
                return File_ERROR
            except IOError:
                return IO_ERROR

        '''if algo == 'MARCA':
            try:
                self.ifd = open(File, 'rb')
                self.ofd = open(splitext(File)[0] + '.mfai', 'wb') if self.oper == 1 else open(splitext(File)[0], 'wb')
            except FileNotFoundError:
                return File_ERROR
            except IOError:
                return IO_ERROR
        else:
            try:
                self.ifd = open(File, 'rb')
                self.ofd = open(splitext(File)[0] + '.fai', 'wb') if self.oper == 1 else open(splitext(File)[0], 'wb')
            except FileNotFoundError:
                return File_ERROR
            except IOError:
                return IO_ERROR
        '''


    def __Prepare_Cipher(self):
        self.BlockCipher = None

    def encrypt(self):
        chunksize = 64 * 1024

        self.ofd.write(self.c_headers)

        while True:
                    chunk = self.ifd.read(chunksize)
                    if len(chunk) == 0:
                        break
                    elif len(chunk) % self.block_size != 0:
                        chunk += b' ' * (self.block_size - len(chunk) % self.block_size)
                    self.ofd.write(self.BlockCipher.encrypt(chunk))
        del chunk ; del chunksize
        self.ofd.close()
        self.ifd.close()
    def decrypt(self):
        chunksize = 24 * 1024
        while True:
                chunk = self.ifd.read(chunksize)
                if len(chunk) == 0:
                    break
                self.ofd.write(self.BlockCipher.decrypt(chunk))

        self.ofd.close()
        self.ifd.close()
    update = pyqtSignal(int)
    def run(self):
        operation = [self.decrypt,self.encrypt]
        operation[self.oper]()
        self.update.emit(SUCCESS)
        sleep(.2)

