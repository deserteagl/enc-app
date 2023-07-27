from constants import KDF,OEAP,algorithms
from struct import  unpack
from Crypto.Cipher import PKCS1_OAEP
class headers:

    def write_headers(fd, headers ,Privacy : str ,algo='AES'):
        if Privacy == 'SGN':
            fd.write(OEAP)
            ksize , signature , gk_hash = headers            # headers = [keysize, signature , priv key hash]
            fd.write(algorithms[algo])                      #write type of algo
            fd.write(ksize)                                 #write rsa ksize
            fd.write(signature)                             #write signed hash of derived keys
            fd.write(gk_hash)                               #write generated hash of priv key

        elif Privacy == 'KDF':
            fd.write(KDF)
            fd.write(algorithms[algo])
            Pass_hash = headers[0]              #headers = [pass_hash, ]
            fd.write(Pass_hash)

    def read_headers(fd):
        k_derivesion = fd.read(4)                        #read algo KDF or PSS
        algo = fd.read(5)

        if k_derivesion == OEAP:
            Key_Size = unpack('h', fd.read(2))[0] + 1
            signature = fd.read(Key_Size)            #perform procedure 32 if KDF sizeof(key) if PSS
            gk_hash = fd.read(32)                    #read signed hash of derived keys
            headers = [signature, gk_hash]
        elif k_derivesion == KDF:
            Pass_hash = fd.read(32)


        return headers,algo


