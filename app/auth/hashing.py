from passlib.context import CryptContext

pwd_cryptcontext = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password:str) -> str:
    return pwd_cryptcontext.hash(password)

def verify_password(password:str,hashed_password:str) -> bool:
    return pwd_cryptcontext.verify(password,hashed_password)






# import bcrypt

# plain_password = b"14092003"
# salt = bcrypt.gensalt()
# hashed_password = bcrypt.hashpw(plain_password,salt)
# print(hashed_password)