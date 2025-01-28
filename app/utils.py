from passlib.context import CryptContext

# Initialize CryptContext with pbkdf2_sha256
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")  # Use pbkdf2_sha256

def hash_password(password: str) -> str:
    """Hashes a plain text password."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain text password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)
