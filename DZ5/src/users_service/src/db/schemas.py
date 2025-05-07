from pydantic import BaseModel, Field


class UserCreateRequest(BaseModel):
    login: str = Field(..., examples=["johndoe"])
    password: str = Field(..., examples=["secret"])
    name: str = Field(..., examples=["John"])


class UserResponse(BaseModel):
    id: int
    login: str
    name: str

    class Config:
        from_attributes = True


class TokenRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
