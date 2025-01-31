from fastapi import FastAPI, HTTPException, Depends, status, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.openapi.utils import get_openapi
import sqlite3
from datetime import timedelta
from models import User, Task, Category
from database import get_db_connection
from auth import create_access_token, get_current_user, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, \
    oauth2_scheme
from utils import hash_password, verify_password

app = FastAPI(
    title="Task Management API",
    description="API for managing tasks, users, and categories",
    version="1.0.0",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Task Management API",
        version="1.0.0",
        description="API for managing tasks, users, and categories",
        routes=app.routes,
    )

    # Merge existing components with security schemes
    components = openapi_schema.get("components", {})
    components.setdefault("securitySchemes", {}).update({
        "OAuth2PasswordBearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    })
    openapi_schema["components"] = components

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi



# User registration
@app.post("/register")
def register(user: User):
    conn = get_db_connection()
    cursor = conn.cursor()
    hashed_password = hash_password(user.password)
    try:
        cursor.execute('''
            INSERT INTO users (username, email, password, role)
            VALUES (?, ?, ?, ?)
        ''', (user.username, user.email, hashed_password, user.role))
        conn.commit()
        user_id = cursor.lastrowid
        return {"id": user_id, "username": user.username, "email": user.email, "role": user.role}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Username or email already exists")
    finally:
        conn.close()


# User login
@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (form_data.username,))
    user = cursor.fetchone()
    conn.close()
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"], "role": user["role"]},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# Admin-only endpoint
@app.get("/admin")
def admin_only(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return {"message": "Welcome, admin!"}


# Create a category (protected endpoint)
@app.post("/categories")
def create_category(category: Category, current_user: dict = Depends(get_current_user)):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO categories (name)
            VALUES (?)
        ''', (category.name,))
        conn.commit()
        category_id = cursor.lastrowid
        return {"id": category_id, "name": category.name}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Category already exists")
    finally:
        conn.close()


# Create a task (protected endpoint)
@app.post("/tasks")
def create_task(task: Task, current_user: dict = Depends(get_current_user)):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO tasks (title, description, status, priority, user_id, category_id)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (task.title, task.description, task.status, task.priority, current_user["id"], task.category_id))
        conn.commit()
        task_id = cursor.lastrowid
        return {"id": task_id, **task.dict()}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Invalid user_id or category_id")
    finally:
        conn.close()


# Get all tasks with pagination (protected endpoint)
@app.get("/tasks")
def get_tasks(
        page: int = Query(1, ge=1, description="Page number (starting from 1)"),
        limit: int = Query(10, ge=1, le=100, description="Number of tasks per page (max 100)"),
        current_user: dict = Depends(get_current_user)
):
    conn = get_db_connection()
    cursor = conn.cursor()

    offset = (page - 1) * limit

    cursor.execute('SELECT * FROM tasks WHERE user_id = ? LIMIT ? OFFSET ?',
                   (current_user["id"], limit, offset))
    tasks = cursor.fetchall()

    cursor.execute('SELECT COUNT(*) FROM tasks WHERE user_id = ?', (current_user["id"],))
    total_items = cursor.fetchone()[0]
    total_pages = (total_items + limit - 1) // limit

    conn.close()

    if not tasks:
        return {
            "tasks": [],
            "message": "No tasks found.",
            "pagination": {
                "total_items": total_items,
                "total_pages": total_pages,
                "current_page": page,
                "items_per_page": limit
            }
        }

    return {
        "tasks": tasks,
        "pagination": {
            "total_items": total_items,
            "total_pages": total_pages,
            "current_page": page,
            "items_per_page": limit
        }
    }


# Get tasks for a specific user (protected endpoint)
@app.get("/users/{user_id}/tasks")
def get_user_tasks(user_id: int, current_user: dict = Depends(get_current_user)):
    if user_id != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized to access these tasks")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE user_id = ?', (user_id,))
    tasks = cursor.fetchall()
    conn.close()

    if not tasks:
        return {"tasks": [], "message": "No tasks found for this user."}

    return {"tasks": tasks}


# Get all users (protected endpoint)
@app.get("/users")
def get_users(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()

    if not users:
        return {"users": [], "message": "No users found."}

    return {"users": users}


# Get a specific user (protected endpoint)
@app.get("/users/{user_id}")
def get_user(user_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return dict(user)


# Get all categories (protected endpoint)
@app.get("/categories")
def get_categories(current_user: dict = Depends(get_current_user)):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM categories')
    categories = cursor.fetchall()
    conn.close()

    if not categories:
        return {"categories": [], "message": "No categories found."}

    return {"categories": categories}


# Get a specific category (protected endpoint)
@app.get("/categories/{category_id}")
def get_category(category_id: int, current_user: dict = Depends(get_current_user)):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM categories WHERE id = ?', (category_id,))
    category = cursor.fetchone()
    conn.close()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    return dict(category)