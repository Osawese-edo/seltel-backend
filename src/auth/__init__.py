from ..config import get_settings

settings = get_settings()

pwd_context = None
oauth2_scheme = None


def _init_auth():
    global pwd_context, oauth2_scheme
    if pwd_context is not None:
        return

    from passlib.context import CryptContext
    from fastapi.security import OAuth2PasswordBearer

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_pwd_context():
    _init_auth()
    return pwd_context


def get_oauth2_scheme():
    _init_auth()
    return oauth2_scheme
