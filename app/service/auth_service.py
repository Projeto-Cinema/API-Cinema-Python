from datetime import datetime, timedelta
from typing import Optional

from jose import jwt

SECRET_KEY = "12312KAS0-SAD"
ALGORITHM = "HS256"

class AuthService:
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=30)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

        return encoded_jwt
    
auth_service = AuthService()