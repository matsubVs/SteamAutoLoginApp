from cryptography.fernet import Fernet

path = r'files/crypto.txt'


def create_key():
    key = Fernet.generate_key()
    print(str(key))
    with open(path, 'r') as f:
        if not f.read():
            with open(path, 'w') as f:
                f.write(str(key)[2:-1])
            print("EMPTY!")
        else:
            return


def extract_key() -> str:
    with open(path) as key_file:
        crypt_line = key_file.readline()

        return crypt_line


class CryptoGraphy(Fernet):

    def __init__(self, cipher_key: str):
        super().__init__(cipher_key.encode('utf-8'))

    def encrypt_string(self, data: str) -> bytes:
        data = data.encode('utf-8')
        bytes_repr = bytes(data)

        return self.encrypt(bytes_repr)

    def decrypt_string(self, string) -> str:
        if isinstance(string, tuple):
            string = string[0]
        print('CRYPTO', string)
        string = string.encode('utf-8')

        string = bytes(string)
        dec_string = self.decrypt(string)

        return str(dec_string)[2:-1]


create_key()
ext_key = extract_key()
crypto_sys = CryptoGraphy(ext_key)
