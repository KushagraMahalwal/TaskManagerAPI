# Task Manager API Documentation

## Overview

The **Task Manager API** is a RESTful service for managing tasks with user authentication and permissions.

* **Admins** can manage all tasks.
* **Regular users** can manage only their own tasks.
* Supports **CRUD operations**, **pagination**, and **JWT authentication**.

## Base URL

```
http://127.0.0.1:8000/api/
```

## Authentication

### 1. Register User

**Endpoint:** `POST /auth/register/` **Description:** Create a new user.
**Request Body (JSON):**

```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepassword"
}
```

**Response:**

```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com"
}
```

### 2. Login User

**Endpoint:** `POST /auth/login/` **Description:** Authenticate user and get JWT tokens.
**Request Body (JSON):**

```json
{
  "email": "john@example.com",
  "password": "securepassword"
}
```

**Response:**

```json
{
  "refresh": "<refresh_token>",
  "access": "<access_token>",
  "user": {
    "id": 1,
    "email": "john@example.com",
    "username": "john_doe"
  }
}
```

> **Note:** Use the `access` token in the `Authorization` header for all protected endpoints:

```
Authorization: Bearer <access_token>
```

## Task Endpoints

### 1. List Tasks

**Endpoint:** `GET /api/tasks/`
**Permission:** Authenticated users

* Admins see all tasks
* Regular users see only their own tasks
* Supports pagination and filtering by completion

**Query Parameters:**

* `page`: Page number (default = 1)
* `page_size`: Number of tasks per page (default = 10, max = 100)
* `completed`: Filter tasks by completion status (`true` / `false`)

**Example:**

```
GET /api/tasks/?page=1&page_size=10&completed=false
Authorization: Bearer <access_token>
```

**Response:**

```json
{
  "count": 12,
  "next": "http://127.0.0.1:8000/api/tasks/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Buy groceries",
      "description": "Milk, Eggs, Bread",
      "completed": false,
      "user": 1,
      "created_at": "2025-09-17T14:00:00Z",
      "updated_at": "2025-09-17T14:00:00Z"
    }
  ]
}
```

### 2. Task Detail / Update / Delete

**Endpoint:** `/api/task_details/?task_id=<id>`
**Permission:** `IsAdminOrOwner`

* Admins can access all tasks
* Regular users can only access their own tasks

#### Get Task

```
GET /api/task_details/?task_id=1
```

**Response:**

```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, Eggs, Bread",
  "completed": false,
  "user": 1,
  "created_at": "2025-09-17T14:00:00Z",
  "updated_at": "2025-09-17T14:00:00Z"
}
```

#### Update Task

```
PUT /api/task_details/?task_id=1
```

**Request Body (JSON):**

```json
{
  "completed": true,
  "title": "Buy groceries updated"
}
```

**Response:**

```json
{
  "id": 1,
  "title": "Buy groceries updated",
  "description": "Milk, Eggs, Bread",
  "completed": true,
  "user": 1,
  "created_at": "2025-09-17T14:00:00Z",
  "updated_at": "2025-09-17T14:05:00Z"
}
```

#### Delete Task

```
DELETE /api/task_details/?task_id=1
```

**Response (204 No Content):**

```json
{
  "message": "Task deleted successfully"
}
```

**Errors:**

* Missing `task_id` → `400 Bad Request`
* Task not found → `404 Not Found`
* Unauthorized → `403 Forbidden` (for regular users trying to delete others’ tasks)

## Permissions

| Permission Class  | Behavior                                                    |
| ----------------- | ----------------------------------------------------------- |
| `IsAuthenticated` | Only logged-in users can access                             |
| `IsAdminOrOwner`  | Admins can access all objects; regular users only their own |
|                   |                                                             |

## Pagination

* **Default page size:** 10
* **Override:** `page_size` query param (max 100)
* **Example:** `/api/tasks/?page=2&page_size=10`

## Testing

* Tests are written using \*\*Django \*\***`APITestCase`** and **DRF APIClient**
* Run tests:

```bash
python manage.py test
```

* Covers:

  * Login & Registration
  * Task CRUD (create, retrieve, update, delete)
  * Permissions (admin vs normal user)
  * Task not found scenarios
  * Pagination & filtering

## Notes

* All endpoints require **JWT authentication** (except register/login).
* Use `Authorization: Bearer <access_token>` in headers.
* Object-level permissions are enforced in `TaskManagerDetailsView` via `check_object_permissions`.

########################################################################################################
Running Tests

Your Task Manager API includes unit tests for all endpoints. Follow these steps to run them:

1. Activate the virtual environment
source tmvenv/bin/activate   # Linux/macOS
# or
tmvenv\Scripts\activate     # Windows

2. Run all tests
python manage.py test

Django will create a temporary test database, run all test cases, and then destroy the test database.

Expected output for passing tests:
.......
Ran 7 tests in 6.652s
OK
Destroying test database for alias 'default'...

3. Run tests for a specific app
python manage.py test api

4. Run a specific test class or method
# All tests in TaskManagerAPITest
python manage.py test api.tests.TaskManagerAPITest

# Only a specific test method
python manage.py test api.tests.TaskManagerAPITest.test_create_task
