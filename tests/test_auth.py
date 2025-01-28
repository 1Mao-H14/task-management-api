from datetime import timedelta
from app.auth import create_access_token, SECRET_KEY, ALGORITHM
from jose import jwt

def test_create_access_token():
    # Test token creation
    data = {"sub": "test_user", "role": "user"}
    expires_delta = timedelta(minutes=30)
    token = create_access_token(data, expires_delta)
    decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded["sub"] == "test_user"
    assert decoded["role"] == "user"