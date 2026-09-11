\# Event-Driven Order \& Inventory Management System



A distributed backend microservice architecture featuring transactional order processing, pessimistic inventory locking, stateless JWT authentication, and cloud-native container orchestration.



\---



\## Architecture \& Engineering Highlights



\* \*\*Stateless Auth \& RBAC:\*\* User authentication using `bcrypt` password hashing and signed `JWT` access tokens containing role-based claims (`customer`, `admin`).

\* \*\*Concurrency Control:\*\* Mitigated race conditions and stock overselling under high concurrency via database row-level locking (`SELECT ... FOR UPDATE`).

\* \*\*Multi-Stage Containerization:\*\* Built lean, production-ready `Docker` container images by decoupling build dependencies from the runtime environment.

\* \*\*Orchestration \& Health Probes:\*\* Containerized local services with automated database readiness checks using `Docker Compose`.

\* \*\*Declarative Kubernetes Architecture:\*\* 

&#x20; \* Replicated stateless API pods with declarative rolling restart and self-healing policies.

&#x20; \* Internal inter-service discovery via `ClusterIP` and external exposure via `NodePort`.

&#x20; \* Decoupled environment configs and secrets using `ConfigMaps` and `Secrets`.



\---



\## Tech Stack



\* \*\*Backend:\*\* Python, FastAPI, SQLAlchemy, Pydantic

\* \*\*Security:\*\* JWT (PyJWT), Passlib (Bcrypt)

\* \*\*Database:\*\* PostgreSQL, SQLite

\* \*\*DevOps \& Cloud-Native:\*\* Docker, Docker Compose, Kubernetes (`kubectl`)



\---



\## Setup \& Running



\### 1. Run via Docker Compose

```bash

docker compose up --build -d

