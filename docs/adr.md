# Architecture Decision Record (ADR)

## ADR-001: Backend Framework

**Decision:** Flask

**Alternative:** Django

**Reason:**

Flask was selected because it is lightweight, simple, and I have previous experience using it. It provides enough features for this project and allows me to focus on the project requirements.

Django was not selected because it includes many built-in features that are not necessary for this project and would increase the project complexity.

---

## ADR-002: Database

**Decision:** MySQL

**Alternative:** MongoDB

**Reason:**

MySQL was selected because this project contains many related tables and requires strong relational data management. It also supports transactions, foreign keys, and constraints, which are important for this system.

MongoDB was not selected because this project has a highly relational database structure, making MySQL a more suitable choice.

---

## ADR-003: Frontend

**Decision:** HTML, CSS, and JavaScript

**Alternative:** React

**Reason:**

HTML, CSS, and JavaScript were selected because they are sufficient for the project requirements and keep the application simple.

React was not selected because it would increase the development time and add unnecessary complexity for this project.
