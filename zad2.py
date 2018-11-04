import base64
import itertools
from Crypto.Cipher import AES
from Crypto import Random

alphabet = list('0123456789abcdef')
n = 2
original_key_list = list('79d33a9529216f1372bdda3c21a50fbc8ef7c6e2d0cb4f97b20eb221e3b4a715')

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
unpad = lambda s : s[:-ord(s[len(s)-1:])]

class KeyGen:
    def __init__(self, alphabet, n, key_suffix):
        self.gen = itertools.product(alphabet, repeat=n)
        self.alphabet = alphabet 
        self.n = n
        self.key_suffix = key_suffix
        if len(key_suffix) == 64:
            self.key_suffix = key_suffix[n:]

    def __iter__(self):
        return self

    def next(self):
        while True:
            prefix = list(self.gen.next())
            key = prefix + self.key_suffix
            return ''.join(key)

class AESCipher:
    def __init__(self, iv):
        self.iv = iv.decode('hex')

    def decrypt(self, enc, key):
        enc = base64.b64decode(enc)
        key = key.decode('hex')
        cipher = AES.new(key, AES.MODE_CBC, self.iv )
        return unpad(cipher.decrypt( enc ))

# key_gen = KeyGen(alphabet, n, original_key_list)

cipher = 'tOSVWxXoBNN2t1FrHP4N7ZfzeAz+2E0I/56Wd0KQOBvTyI0Pd7PK51uc/RDKkqacTj8ewyfI+0EslWlyJ8htG1DFkQI6TTcgxNHRVw+9GKrwHfwsb5baqcH0zUxVeMszNM1sSSKknKvUQ/BWojG8QA=='

# alg = AESCipher('d9e4cf593e76c539f70bcfa8c08d1a2c')
# msg = alg.decrypt('tOSVWxXoBNN2t1FrHP4N7ZfzeAz+2E0I/56Wd0KQOBvTyI0Pd7PK51uc/RDKkqacTj8ewyfI+0EslWlyJ8htG1DFkQI6TTcgxNHRVw+9GKrwHfwsb5baqcH0zUxVeMszNM1sSSKknKvUQ/BWojG8QA==',
#     '79d33a9529216f1372bdda3c21a50fbc8ef7c6e2d0cb4f97b20eb221e3b4a715')


def brute_force(n, key_suffix, iv, cipher):
    alg = AESCipher(iv)
    key_gen = KeyGen(alphabet, n, key_suffix)

    while True:
        try:
            key = key_gen.next()
        except StopIteration:
            break

        msg = alg.decrypt(cipher, key)
        try:
            m = msg.decode('utf-8')
        except Exception as e:
            pass
        else:
            if len(m) > 10:
                print m


brute_force(4, original_key_list, 'd9e4cf593e76c539f70bcfa8c08d1a2c'
    , cipher)

