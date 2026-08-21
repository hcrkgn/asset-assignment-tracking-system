# Asset and Assignment Tracking System

[![CI](https://github.com/hcrkgn/asset-assignment-tracking-system/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/hcrkgn/asset-assignment-tracking-system/actions/workflows/ci.yml)

## About

This project was developed as part of the Phase 2 internship program.

The system is designed to manage company assets, employee assignments, maintenance records, inventory counts, asset depreciation, requests, and related reports.

## Technology Stack

- Backend: Flask
- Frontend: HTML, CSS, JavaScript
- Database: MySQL
- ORM: Flask-SQLAlchemy
- Database Migration: Flask-Migrate
- Authentication: Session-based authentication
- Password Security: bcrypt
- Testing: pytest
- Code Quality: Ruff
- Containerization: Docker

## Project Status

- Stage 0 – Analysis and Design (Completed)
- Stage 1 – Project Setup and Authentication (Completed)
- Stage 2 – Asset Card and List (Completed)
- Stage 3 – Assignment and Return (Completed)
- Stage 4 – Requests, Approval Flow and Audit Trail (Completed)
- Stage 5 – QR Labels and Inventory Count (Completed)
- Stage 6 – Maintenance Plan and Scheduled Job (Completed)
- Stage 7 – Depreciation, Reports, Import and Export (Completed)
- Stage 8 – Security and Performance Hardening (Completed)

## Running the Project

The project uses Docker Compose for the application and MySQL database.

```bash
docker compose up --build
```

After the containers start, the application can be accessed through the configured Flask port.

Environment-specific configuration is stored in `.env`. A `.env.example` file is provided for required environment variables.

## Documentation

Project documents are available in the `docs` folder.

Included documents:

- User Stories
- ER Diagram
- State Machine Diagram
- Screen Flow
- Architecture Decision Records (ADR)
- Acceptance Criteria
- Security Review

## Security

The application includes several security measures:

- Password hashing with bcrypt
- Session-based authentication
- Role-based authorization
- CSRF protection
- Brute-force protection and login lockout
- SQL injection protection
- XSS protection through template escaping
- IDOR and authorization checks
- Secure file upload validation
- File extension and MIME type validation
- Upload size limitation
- Sanitized upload filenames
