import secrets
import string

class KeyDicc():
    def __init__(self) -> None:
        self.letters = string.ascii_letters
        self.digits = string.digits
        self.special_chars = string.punctuation

    def getKey(self):
        alphabet = self.letters+self.digits

        pwd_length = 12

        pwd = ''
        for i in range(pwd_length):
            pwd += ''.join(secrets.choice(alphabet))

        return pwd
        
    