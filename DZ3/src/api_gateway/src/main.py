from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
import httpx
from pydantic import BaseModel

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def verify_token(token: str):
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:8000/verify-token", headers={"Authorization": f"Bearer {token}"})
        if response.status_code != 200:
            raise HTTPException(status_code=401, detail="Invalid token")
        return response.json()

@app.post("/register")
async def register(username: str, password: str):
    async with httpx.AsyncClient() as client:
        response = await client.post("http://localhost:8000/register", json={"username": username, "password": password})
        return response.json()

@app.post("/login")
async def login(username: str, password: str):
    async with httpx.AsyncClient() as client:
        response = await client.post("http://localhost:8000/login", json={"username": username, "password": password})
        return response.json()

@app.post("/orders/")
async def create_order(order, token: str = Depends(oauth2_scheme)):
    await verify_token(token)
    async with httpx.AsyncClient() as client:
        response = await client.post("http://localhost:8001/orders/", json=order.dict(), headers={"Authorization": f"Bearer {token}"})
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json())
        return response.json()

@app.get("/orders/")
async def get_orders(token: str = Depends(oauth2_scheme)):
    await verify_token(token)
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:8001/orders/", headers={"Authorization": f"Bearer {token}"})
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json())
        return response.json()


