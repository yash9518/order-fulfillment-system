# Event-Driven Order & Inventory Management System

A distributed backend microservice architecture featuring transactional order processing, pessimistic inventory locking, stateless JWT authentication, database schema migrations with Alembic, and cloud-native Kubernetes orchestration.

---

## Architecture & Engineering Highlights

* **Stateless Auth & RBAC:** User authentication using bcrypt password hashing and signed JWT access tokens. Strict role-based access control enforces `admin` permissions on catalog mutations.
* **Concurrency Control:** Mitigated race conditions and stock overselling under high concurrency via database row-level locking (`SELECT ... FOR UPDATE`).
* **Schema Evolution:** Managed database migrations and version-controlled schema definitions using Alembic.
* **Multi-Stage Containerization:** Built lean production container images by decoupling build dependencies from runtime environments.
* **Automated Test Coverage:** Verified authorization boundaries, RBAC role restrictions, and checkout flows using pytest and HTTPX.
* **Declarative Kubernetes Architecture:**
  * Replicated API pods with self-healing reconciliation.
  * Internal inter-service discovery via ClusterIP and external exposure via NodePort.
  * Decoupled environment configurations and credentials using ConfigMaps and Secrets.

---

## Tech Stack

* **Backend:** Python, FastAPI, SQLAlchemy, Alembic, Pydantic
* **Security:** PyJWT, Bcrypt
* **Database:** PostgreSQL, SQLite
* **DevOps & Cloud-Native:** Docker, Docker Compose, Kubernetes

---

## Quickstart & Local Setup

### 1. Environment Configuration
Copy the example environment template and fill in your own values:
```bash
copy .env.example .env
```
*(On macOS/Linux, use `cp .env.example .env` instead.)*

### 2. Run via Docker Compose
```bash
docker compose up --build -d
```
This starts Postgres and the API together. The database starts empty, so run migrations next.

### 3. Run Database Migrations
With the containers running, apply the schema inside the `web` container:
```bash
docker compose exec web alembic upgrade head
```
The API is now available at `http://localhost:8000`, with interactive docs at `http://localhost:8000/docs`.

### 4. Run Locally Without Docker (optional)
```bash
python -m venv venv
venv\Scripts\activate        # or: source venv/bin/activate on macOS/Linux
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

### 5. Run Tests
```bash
pytest tests/ -v
```