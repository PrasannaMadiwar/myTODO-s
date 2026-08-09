
from jose import jwt
from passlib.context import CryptContext
from apps.api.source.configuration import Settings
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict):
    to_encode = data.copy()
    exp = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": exp})
    return jwt.encode(to_encode, Settings.SECURITY_KEY, algorithm= Settings.ALGORITHM)




def verify_access_token(token: str = Depends(oauth2_scheme)):
    print("Received token:", token)
    try:
        payload = jwt.decode(token, Settings.SECURITY_KEY, algorithms=[Settings.ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        return username
    
    except jwt.JWTError:
         raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )