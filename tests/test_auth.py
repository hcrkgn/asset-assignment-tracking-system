import pytest
from flask import Flask

from app.utils.auth import require_roles


@pytest.fixture
def app():
    application = Flask(__name__)
    application.config["SECRET_KEY"] = "test-secret"
    application.config["TESTING"] = True

    @application.route("/login")
    def login():
        return "Login"

    @application.route("/admin")
    @require_roles(1)
    def admin():
        return "Admin"

    @application.errorhandler(403)
    def forbidden(error):
        return "Forbidden", 403

    return application


@pytest.fixture
def client(app):
    return app.test_client()


def test_unauthenticated_browser_request_redirects_to_login(client):
    response = client.get("/admin")

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/login")


def test_unauthenticated_ajax_request_returns_session_expired_json(client):
    response = client.get(
        "/admin",
        headers={"X-Requested-With": "XMLHttpRequest"},
    )

    assert response.status_code == 401
    assert response.get_json()["error"] == "session_expired"


def test_employee_receives_403_for_admin_route(client):
    with client.session_transaction() as session:
        session["user_id"] = 3
        session["role_id"] = 4

    response = client.get("/admin")

    assert response.status_code == 403
    assert response.data == b"Forbidden"


def test_admin_can_access_admin_route(client):
    with client.session_transaction() as session:
        session["user_id"] = 1
        session["role_id"] = 1

    response = client.get("/admin")

    assert response.status_code == 200
    assert response.data == b"Admin"
