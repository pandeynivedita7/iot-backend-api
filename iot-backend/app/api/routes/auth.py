from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.security import verify_password, create_access_token, hash_password

router = APIRouter(prefix="/auth", tags=["auth"])

# Demo user (local only)
fake_user = {
    "username": "admin",
    "password": hash_password("admin123")
}

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != fake_user["username"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username")

    if not verify_password(form_data.password, fake_user["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")

    token = create_access_token(form_data.username)
    return {"access_token": token, "token_type": "bearer"}