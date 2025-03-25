from fastapi import FastAPI, Depends, HTTPException
import httpx
from .api import router

app = FastAPI()

app.include_router(router)
