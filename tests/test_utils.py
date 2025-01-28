from app.utils import hash_password, verify_password

def test_password_hashing():
    # Test password hashing and verification
    plain_password = "password123"
    hashed_password = hash_password(plain_password)
    assert verify_password(plain_password, hashed_password) == True

def test_invalid_password_verification():
    # Test verification with incorrect password
    plain_password = "password123"
    hashed_password = hash_password(plain_password)
    assert verify_password("wrong_password", hashed_password) == False