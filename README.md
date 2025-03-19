# FastAPI JWT RBAC

A RESTful API built with **FastAPI** that implements **JWT authentication** and **role-based access control (RBAC)**. This project allows users to register, log in, and perform CRUD operations on projects based on their roles (admin or user).

## Features
- **User Registration and Login**: Users can register with a username, password, and role. Passwords are securely hashed using bcrypt.
- **JWT Authentication**: Users receive a JWT token upon login, which is used for authenticating subsequent requests.
- **Role-Based Access Control (RBAC)**:
  - **Admin**: Can create, update, delete, and view projects.
  - **User**: Can only view projects.
- **CRUD Operations**: Basic CRUD operations for a sample resource (projects).

---

## Installation

### Prerequisites
- Python 3.8+
- PostgreSQL
- Git

### Steps
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/fastapi-jwt-rbac.git
   cd fastapi-jwt-rbac
   ```
2. **Set Up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Set Up the Database**:
   Install PostgreSQL and create a database named `fastapi_jwt_rbac`.
   Update the `.env` file with your database credentials.
   ```bash
   pip install -r requirements.txt
   ```
5. **Run the Application**:
   ```bash
   uvicorn app.main:app --reload
   ```
6. **Access the API**:
   Open your browser and navigate to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to view the Swagger UI documentation.

## API Endpoints

### User Registration
#### **POST /register**

**Body**:
```json
{
  "username": "admin",
  "password": "admin123",
  "role": "admin"
}
```

### User Login
#### **POST /login**

**Body**:
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Response**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Projects
1. **GET /projects** (Requires JWT)
   
   Returns a list of all projects.

2. **POST /projects** (Admin only)

**Body**:
```json
{
  "name": "Updated Project A",
  "description": "Updated description"
}
```

3. **PUT /projects/{project_id}** (Admin only)

**Body**:
```json
{
  "name": "Updated Project A",
  "description": "Updated description"
}
```

4. **DELETE /projects/{project_id}** (Admin only)

Deletes the project with the specified ID.

## Testing the API

### Using Postman
1. Import the Postman collection (if available).
2. Set the `base_url` environment variable to `http://127.0.0.1:8000`.
3. Use the `/register` endpoint to create a new user.
4. Use the `/login` endpoint to get a JWT token.
5. Use the token to access protected endpoints (e.g., `/projects`).

## Additional Configurations

### Environment Variables
- `DATABASE_URL`: PostgreSQL connection string.
- `JWT_SECRET_KEY`: Secret key for signing JWT tokens.
- `JWT_ALGORITHM`: Algorithm for JWT token signing (default: HS256).
- `JWT_EXPIRE_MINUTES`: Token expiration time in minutes.

### Deployment
Deploy the API to a cloud platform like Heroku, Render, or AWS.

Set up environment variables in the deployment environment.

