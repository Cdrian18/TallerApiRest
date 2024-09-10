from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from datetime import datetime, timedelta, timezone
from typing import Optional
from utils.config import SECRET_KEY
from utils.database import user_collection, user_helper
from schemas.user import PublicUser

# Configuraciones
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
RECOVERY_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_recovery_token(user_id: str):
    expires_delta = timedelta(minutes=RECOVERY_TOKEN_EXPIRE_MINUTES)
    return create_access_token(data={"sub": user_id}, expires_delta=expires_delta)


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        return user_id
    except jwt.PyJWTError:
        raise credentials_exception

async def get_current_user(token: str = Depends(oauth2_scheme)) -> PublicUser:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user_id = verify_token(token, credentials_exception)
    
    user = await user_collection.find_one({"public_id": user_id})
    if user is None:
        raise credentials_exception
    
    return PublicUser(**user_helper(user))
