from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from backend.app.core import security
router = APIRouter()
@router.post("/login")
async def login_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    return {"access_token": "fake-token", "token_type": "bearer"}
