from hashlib import pbkdf2_hmac,sha256
from constants import PASS_Valid,PASS_Invalid

class KDF:
    def __init__(self,password : str):
        self.password = password

    def __generate_prime(self):
        prime = 1
        N = len(self.password)
        while True:
            if prime % N == 0:
                return prime
            prime += 1


    def __generate_salt(self):
        salt = ""
        m = self.__generate_prime()
        for index,char in enumerate(self.password):
            salt += str((2**index) * len(self.password) * ord(char) % m)
        return salt.encode()

    def generate_key_from_pass(self):
        salt = self.__generate_salt()
        key = pbkdf2_hmac('sha512',self.password.encode(),salt,1000000,64)
        return key

class KDF_Check:
    def check(Password,Pass_hash):
        if sha256(Password.encode()).digest() == Pass_hash:
            return PASS_Valid
        else :
            return PASS_Invalid

    def gen_hash(Password):
        Pass_hash = sha256(Password.encode())
        return Pass_hash
#x= KDF('root').generate_key_from_pass()
#print(x)