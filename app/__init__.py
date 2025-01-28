# app/__init__.py

# Import the FastAPI app and other modules
from .main import app
from .database import get_db_connection
from .auth import create_access_token, get_current_user
from .models import User, Task, Category

# Optional: Define package-level variables or configurations
__version__ = "1.0.0"