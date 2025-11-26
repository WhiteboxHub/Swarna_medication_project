# Medication Management Application

A fullstack **Medication Management** system built with modern cloud-native architecture.
This application allows caregivers to create medications, define dosing schedules, view upcoming doses, and mark doses as taken.
The system is designed for **production deployment on AWS** while remaining **easy to run locally** without a database.

---

## Features

### Core Functionality

- Add and manage medications (inactive instead of delete)
- Define medication schedules
  - Daily
  - Weekly
  - Multiple times per day
- Generate and list upcoming doses
- Mark doses as taken
- View medication details and history

### Non-Functional Features

- Authentication middleware
- API rate limiting
- Repository pattern with pluggable storage
- In-memory / Redis caching
- Unified error handling
- Full unit and integration testing
- AWS-ready deployment (EKS & ECS supported)

---

## Tech Stack

### Backend

- **FastAPI (async)**
- **Pydantic**
- **MongoDB / AWS DocumentDB** (production)
- **IndexedDB / LocalStorage** (local development)
- **Redis** (optional caching)
- **Pytest**

### Frontend

- **React (Create React App)**
- **Redux Toolkit**
- **Tailwind CSS**
- **IndexedDB with LocalStorage fallback**
- **Jest & React Testing Library**

### Infrastructure

- **Docker & Docker Compose**
- **AWS API Gateway**
- **AWS EKS (Helm) or ECS (Fargate)**
- **AWS DocumentDB**
- **GitHub Actions CI/CD**

---

## Project Structure



root/

├── backend/

│   ├── app/

│   │   ├── api/routes/

│   │   ├── core/

│   │   ├── db/

│   │   ├── services/

│   │   ├── tests/

│   │   └── main.py

│   └── Dockerfile

│

├── frontend/

│   ├── src/

│   │   ├── components/

│   │   ├── pages/

│   │   ├── store/

│   │   ├── hooks/

│   │   └── tests/

│   └── Dockerfile

│

├── infra/

│   ├── docker-compose.yml

│   ├── eks/helm/medication-manager/

│   └── ecs/

│

├── db.sql

└── README.md


