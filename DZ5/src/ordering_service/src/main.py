from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from .db.db import ensure_indices
from .api import orders_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await ensure_indices()
    yield

app = FastAPI(
    title="Orders Service",
    lifespan=lifespan,
)
app.include_router(orders_router.router)


if __name__ == "__main__":
    uvicorn.run("main:main_app", host="0.0.0.0", port=8000, reload=True)
