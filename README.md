# Blog API Platform

A robust, RESTful backend service built with **FastAPI** that powers a complete blogging platform. It provides secure user authentication, role-based access controls for resource ownership, and highly efficient data retrieval with advanced features like pagination and search filtering.

This project demonstrates strong backend engineering principles, including database modeling, API design, security, and state management.

---

## 🚀 Features

- **User Authentication (JWT):** Secure login endpoint issuing JSON Web Tokens for stateless authentication.
- **Resource Ownership Authorization:** Strict permission checks ensuring users can only edit or delete the blog posts they authored.
- **Advanced Querying:** Implements efficient pagination and dynamic substring search functionality for retrieving blog lists.
- **Full CRUD Operations:** Comprehensive endpoints to Create, Read, Update, and Delete blog posts.
- **Data Validation & Serialization:** Utilizes Pydantic schemas for robust request validation and response formatting.
- **ORM Integration:** Uses SQLAlchemy for abstract database interactions, making the application database-agnostic (easily switchable between SQLite and PostgreSQL).

---

## 🛠️ Tech Stack

- **Framework:** FastAPI (Python)
- **Database ORM:** SQLAlchemy
- **Data Validation:** Pydantic
- **Authentication:** JWT (JSON Web Tokens), passlib, python-jose
- **Server:** Uvicorn
- **Environment Management:** python-dotenv

---

## 🏗️ Architecture & Workflow

1. **Authentication Flow:** 
   - A user submits their credentials to `/login`.
   - The system verifies the user against the database and returns a signed JWT.
   - For protected routes, the client includes the JWT in the `Authorization` header.
2. **Blog Management (CRUD):**
   - **Create:** Authenticated users can create new posts, which are automatically linked to their User ID (`owner_id`).
   - **Read:** Any user can fetch a list of blogs or a specific blog. List endpoints support `?page=X&limit=Y` for pagination and `?search=term` for filtering.
   - **Update/Delete:** Validates the JWT and additionally verifies that the requester's ID matches the blog's `owner_id` before committing changes to the database.

---

## 📖 API Endpoints

### Authentication
- `POST /login`: Authenticate user and receive a JWT token.

### Blog Management
- `POST /blogs`: Create a new blog post. *(Requires Authentication)*
- `GET /blogs`: Retrieve a paginated list of blog posts. Supports `page`, `limit`, and `search` query parameters.
- `GET /blogs/{blog_id}`: Retrieve details of a specific blog post by its ID.
- `PUT /blogs/{blog_id}`: Update an existing blog post. *(Requires Authentication & Ownership)*
- `DELETE /blogs/{blog_id}`: Delete a blog post. *(Requires Authentication & Ownership)*

---

## ⚙️ Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/Parth2632/Blog_API.git
cd Blog_API
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory and add the following:
```env
DATABASE_URL=sqlite:///./blog.db  # Or your PostgreSQL connection string
secretkey=YOUR_SUPER_SECRET_KEY
algorithm=HS256
accesstokentime=30
```

### 5. Run the Application
```bash
uvicorn main:app --reload
```
The API will be available at `http://localhost:8000`. 
You can interact with the auto-generated Swagger UI documentation at `http://localhost:8000/docs`.

---

