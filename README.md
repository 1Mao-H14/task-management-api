# Task Management API

This is a **Task Management API** built using **FastAPI** and **SQLite**, designed to help users efficiently manage their tasks with features like authentication, task categorization, and pagination.

## Features

- **User Management**:
  - Register new users with unique usernames and email addresses.
  - Secure login using JWT-based authentication.
  - Role-based access control (e.g., `admin` vs `user`).
  
- **Task Management**:
  - Create, read, update, and delete tasks.
  - Assign tasks to specific categories.
  - Set task priorities and statuses.

- **Category Management**:
  - Create custom categories for better task organization.
  - Fetch all categories or a specific category.

- **Pagination**:
  - Fetch tasks in paginated format for better performance.
  - Customize page size and number.

- **Authentication & Security**:
  - Secure endpoints with JWT-based authentication.
  - Passwords are hashed using industry-standard algorithms.

- **Admin Functionality**:
  - View all registered users.
  - Access and manage all tasks in the system.

---

## Installation

### Prerequisites
Make sure you have the following installed:
- Python 3.9 or higher
- Git (for cloning the repository)

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/1Mao-H14/task-management-api.git
   ```

2. Navigate to the project directory:
   ```bash
   cd task-management-api
   ```

3. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

4. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

5. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

### Running the Server

1. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

2. Open your browser and access the API:
   - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## API Endpoints

### Authentication
- `POST /register` – Register a new user.
- `POST /token` – Obtain an access token for login.

### Tasks
- `GET /tasks` – Fetch all tasks (with pagination).
- `POST /tasks` – Create a new task.
- `GET /tasks/{task_id}` – Fetch a specific task.
- `PUT /tasks/{task_id}` – Update a task.
- `DELETE /tasks/{task_id}` – Delete a task.

### Categories
- `GET /categories` – Fetch all categories.
- `POST /categories` – Create a new category.

### Users (Admin Only)
- `GET /users` – Fetch all registered users.
- `GET /users/{user_id}` – Fetch details of a specific user.

---

## Configuration

### Environment Variables
Modify the following variables in the `auth.py` file for security:
- `SECRET_KEY`: Replace with a secure random string.
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Set the token expiration time.

---

## Testing the API

1. Use an API client like **Postman** or **cURL** to interact with the endpoints.
2. Example: To get an access token, send a `POST` request to `/token` with:
   ```json
   {
       "username": "your_username",
       "password": "your_password"
   }
   ```
3. Include the token in the `Authorization` header for protected endpoints:
   ```bash
   Authorization: Bearer <access_token>
   ```

---

## Project Structure

```
task-management-api/
├── app/
│   ├── __init__.py
│   ├── auth.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── utils.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_api.py
│   ├── test_auth.py
│   ├── test_database.py
│   └── test_utils.py
├── test_env/          # Test environment directory == u can use it if you like
├── README.md
└── requirements.txt
```

---

## Contribution

This project was developed by **Marouan Hamdaoui** in collaboration with the **ALX Organization** in the year **2025**.

Feel free to fork the repository and contribute enhancements!

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.


    
