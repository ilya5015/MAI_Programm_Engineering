from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional, Dict
from ..models.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

fake_users_db: Dict[str, str] = {}

class UserController:
    def __init__(self):
        self.users_db = fake_users_db

    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
            to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    def create_admin_user(self):
        admin_username = "admin"
        admin_password = "secret"
        if admin_username not in self.users_db:
            self.users_db[admin_username] = self.hash_password(admin_password)
            print("Admin user created successfully.")

    def register_user(self, user: User):
        if user.username in self.users_db:
            raise HTTPException(status_code=400, detail="Username already registered")
        self.users_db[user.username] = self.hash_password(user.password)
        return {"msg": "User  registered successfully"}

    def login_user(self, user: User):
        if user.username not in self.users_db or not self.verify_password(user.password, self.users_db[user.username]):
            raise HTTPException(status_code=400, detail="Invalid username or password")
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = self.create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
        return {"access_token": access_token, "token_type": "bearer"}

    def verify_token(self, token: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return {"username": payload["sub"]}
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")