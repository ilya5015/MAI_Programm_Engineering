from fastapi import FastAPI, HTTPException, Depends
from passlib.context import CryptContext
from jwt import encode, decode
from datetime import datetime, timedelta
from typing import Optional
from .api import router

app = FastAPI()

app.include_router(router)

