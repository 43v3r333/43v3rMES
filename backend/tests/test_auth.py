import pytest
from backend.app.core.security import verify_password, get_password_hash
def test_password_hashing():
    password = "secretpassword"
    hashed = get_password_hash(password)
    assert verify_password(password, hashed) is True
def test_token_creation():
    from backend.app.core.security import create_access_token
    from jose import jwt
    from backend.app.core.config import settings
    token = create_access_token("test-user")
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    assert payload["sub"] == "test-user"
