import sqlite3
from app.database import get_db_connection

def test_database_connection():
    # Test database connection
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1")
    result = cursor.fetchone()
    assert result[0] == 1
    conn.close()

def test_database_schema():
    # Test if the tasks table exists
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tasks'")
    result = cursor.fetchone()
    assert result is not None  # Ensure the tasks table exists
    conn.close()