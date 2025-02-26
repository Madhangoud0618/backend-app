# Project README

Welcome to the **Referral-Based User Registration API**! This API allows users to register, log in, and manage referral codes. It supports password reset functionality and a referral statistics endpoint for users.

## 🚀 Getting Started

Follow these steps to get your project up and running locally.

### Prerequisites

Make sure you have the following installed:
- Python 3.8+
- `pip` (Python's package installer)
- Virtual Environment (recommended)

### Setup

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/referral-api.git
    cd referral-api
    ```

2. **Create a Virtual Environment:**
    ```bash
    python3 -m venv .venv
    ```

3. **Activate the Virtual Environment:**
    - On Windows:
      ```bash
      .\.venv\Scripts\activate
      ```
    - On macOS/Linux:
      ```bash
      source .venv/bin/activate
      ```

4. **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5. **Configure environment variables:**

    Create a `.env` file at the root of the project and add your configuration like this:

    ```bash
    DATABASE_URL=sqlite+aiosqlite:///./test.db  # Change this to your actual database URL
    SECRET_KEY=your-secret-key-here
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    EMAIL_SENDER=your-email@example.com
    ```

### Run the Application

To start the FastAPI app with automatic reloading, use the following command:

```bash
uvicorn app.main:app --reload
```

This will run the app locally at `http://127.0.0.1:8000`. You can now access the API and test its functionality.

---

## 🧑‍💻 API Endpoints

Here are the available endpoints and their descriptions:

### Authentication

- **POST /register**
    - **Description**: Register a new user with an optional referral code.
    - **Body**:
    ```json
    {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "password123",
        "referral_code": "existing-referral-code"  // Optional
    }
    ```
    - **Response**:
    ```json
    {
        "id": 1,
        "username": "newuser",
        "email": "newuser@example.com",
        "referral_code": "generatedReferralCode",
        "referred_by": null,
        "created_at": "2025-02-26T12:34:56+00:00"
    }
    ```

- **POST /login**
    - **Description**: Log in using a username and password.
    - **Body**:
    ```json
    {
        "username": "newuser",
        "password": "password123"
    }
    ```
    - **Response**:
    ```json
    {
        "access_token": "your_jwt_token",
        "token_type": "bearer"
    }
    ```

- **POST /forgot-password**
    - **Description**: Request a password reset link.
    - **Body**:
    ```json
    {
        "email": "newuser@example.com"
    }
    ```
    - **Response**:
    ```json
    {
        "message": "Password reset instructions sent"
    }
    ```

- **POST /reset-password**
    - **Description**: Reset the password with the received token.
    - **Body**:
    ```json
    {
        "token": "reset_token",
        "new_password": "newpassword123"
    }
    ```
    - **Response**:
    ```json
    {
        "message": "Password updated successfully"
    }
    ```

### Referrals

- **GET /referrals**
    - **Description**: Get the list of referrals for the current user.
    - **Response**:
    ```json
    [
        {
            "id": 1,
            "referrer_id": 1,
            "referred_user_id": 2,
            "date_referred": "2025-02-26T12:34:56+00:00",
            "status": "successful"
        }
    ]
    ```

- **GET /referral-stats**
    - **Description**: Get referral statistics for the current user.
    - **Response**:
    ```json
    {
        "total_referrals": 5,
        "active_referrals": 3,
        "pending_referrals": 2
    }
    ```

---

## 🎯 Example Usage with `curl`

### 1. Register a new user

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/register' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "newuser",
  "email": "newuser@example.com",
  "password": "password123"
}'
```

### 2. Log in to get a JWT token

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/login' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username=newuser&password=password123'
```

### 3. Forgot Password (Request reset link)

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/forgot-password' \
  -H 'Content-Type: application/json' \
  -d '{
  "email": "newuser@example.com"
}'
```

### 4. Reset Password (Using token)

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/reset-password' \
  -H 'Content-Type: application/json' \
  -d '{
  "token": "your_reset_token",
  "new_password": "newpassword123"
}'
```

### 5. Get Referral Stats

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/referral-stats' \
  -H 'Authorization: Bearer your_jwt_token'
```

---

## ⚙️ Project Structure

```
.
├── app
│   ├── core
│   │   ├── config.py         # Application settings and configurations
│   ├── database.py           # Database connection and session management
│   ├── models                # ORM models for users and referrals
│   ├── routers               # API routers for handling user/auth and referral routes
│   ├── schemas               # Pydantic models for input/output validation
│   ├── utils                 # Utility functions for helpers and security
├── requirements.txt          # Project dependencies
└── .gitignore                # Files/folders to ignore
```

---

## 📝 Conclusion

This API allows you to manage users, handle user registrations with referral codes, and provides functionalities for password resets and referral statistics. With this simple yet powerful setup, you can quickly build and extend a referral-based application.

Happy coding! 😊
