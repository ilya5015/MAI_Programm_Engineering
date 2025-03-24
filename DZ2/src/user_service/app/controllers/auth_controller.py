from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.dependencies.auth import create_access_token, client_db, pwd_context

class AuthController:
    def __init__(self):
        self.router = APIRouter(tags=["auth"])
        self.router.add_api_route("/token", self.login_for_access_token, methods=["POST"])

    async def login_for_access_token(self, form_data: OAuth2PasswordRequestForm = Depends()):
        password_check = False
        if form_data.username in client_db:
            password = client_db[form_data.username]
            if pwd_context.verify(form_data.password, password):
                password_check = True

        if password_check:
            access_token_expires = timedelta(minutes=30)
            access_token = create_access_token(data={"sub": form_data.username}, expires_delta=access_token_expires)
            return {"access_token": access_token, "token_type": "bearer"}
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

auth_controller = AuthController()