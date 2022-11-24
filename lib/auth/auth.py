from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# TODO move to .env & config.py
SECRET_KEY = "f81f7701c26580976e05c4a85c072d6103d414a9f52431542c3e9289d11e6337"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
