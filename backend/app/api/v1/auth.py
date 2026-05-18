from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
router = APIRouter()
@router.post("/login")
async def login_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    return {"access_token": "fake-token", "token_type": "bearer"}
