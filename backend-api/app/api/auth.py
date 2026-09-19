from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from ..core import security

router = APIRouter()

# For skeleton: single demo user
_DEMO_USER = {"username": "demo", "hashed_password": security.get_password_hash("demo123")}


@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != _DEMO_USER["username"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    if not security.verify_password(form_data.password, _DEMO_USER["hashed_password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

    access_token = security.create_access_token({"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}
