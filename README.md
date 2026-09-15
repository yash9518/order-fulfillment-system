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
Copy the example environment file:
```bash
cp .env.example .env