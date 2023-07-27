from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA
from constants import *
from struct import pack
class Signature():
    def Verify(Crypted_data,priv_key_file : str ):
        try:
            priv_key_fd = open(priv_key_file,'rb')
            pkey = RSA.importKey(priv_key_fd.read())
        except FileNotFoundError:
            return File_ERROR
        except IOError:
            return IO_ERROR


        Verifier = PKCS1_OAEP.new(pkey)

        try:
            data = Verifier.decrypt(Crypted_data)
            return SUCCESS,data
        except ValueError:
            return VERIFY_FALSE,None

    def decrypt_Signature(Crypted_data,priv_key_file : str):
            priv_key_fd = open(priv_key_file, 'rb')
            pkey = RSA.importKey(priv_key_fd.read())

            Verifier = PKCS1_OAEP.new(pkey)

            return Verifier.decrypt(Crypted_data)


    def Sign(hdata,pub_key_file):
        try:
            pub_key_fd = open(pub_key_file, 'rb')
            Pub_Key = RSA.importKey(pub_key_fd.read())
        except FileNotFoundError:
            return File_ERROR
        except IOError:
            return IO_ERROR

        Signature = b''
        Signer = PKCS1_OAEP.new(Pub_Key)
        for i in hdata:
            Signature = Signature+ i
        Signature = Signer.encrypt(Signature)
        return Signature

def check_key_valid(keyfile):
    with open(keyfile) as e:
        try:
            k=RSA.importKey(e.read())
            return k.size_in_bits()
        except:
            return File_ERROR
