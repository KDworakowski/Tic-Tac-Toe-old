from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hashing():
    def bcrypt(password):
        return pwd_cxt.hash(password)
