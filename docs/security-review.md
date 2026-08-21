# Security Review

## 1. Authentication

- Passwords are hashed.
- Failed login attempts are limited.
- Account lockout is applied after 20 failed attempts.
- Lock duration is 15 minutes.

## 2. Authorization

- Role-based authorization is implemented.
- Unauthorized users receive 403.
- Department managers can only access requests from their department.

## 3. CSRF Protection

- Flask-WTF CSRF protection is enabled.
- All POST forms contain CSRF tokens.
- Requests without a valid token are rejected.

## 4. XSS Protection

- Jinja autoescaping is enabled.
- No unsafe |safe, Markup(), innerHTML or outerHTML usage was found.

## 5. SQL Injection

- Database queries use SQLAlchemy or parameterized queries.
- User input is not directly concatenated into SQL queries.

## 6. File Upload Security

- Allowed extensions are restricted.
- MIME types are checked.
- Upload size is limited to 50 MB.
- Uploaded filenames are sanitized.
- UUIDs are used for stored filenames.

## 7. IDOR Protection

- Resource IDs are checked before access.
- Role authorization is applied to protected routes.
- Department ownership is checked for manager requests.
