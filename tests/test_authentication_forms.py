import os
import tempfile

import pytest

from app import app


@pytest.fixture
def client():
    db_fd, app.config["DATABASE"] = tempfile.mkstemp()
    app.config["TESTING"] = True

    with app.test_client() as client:
        # with app.app_context():
        #     init_db()
        yield client

    os.close(db_fd)
    os.unlink(app.config["DATABASE"])


def login(client, username, password):
    return client.post(
        "/login", data=dict(username=username, password=password), follow_redirects=True
    )


def logout(client):
    return client.get("/logout", follow_redirects=True)


def test_login_logout(client):
    """Make sure login and logout works."""

    rv = login(client, "andrewr", "password123")
    assert b"You were logged in" in rv.data

    rv = logout(client)
    assert b"You were logged out" in rv.data

    rv = login(client, app.config["USERNAME"] + "x", app.config["PASSWORD"])
    assert b"Invalid username" in rv.data

    rv = login(client, app.config["USERNAME"], app.config["PASSWORD"] + "x")
    assert b"Invalid password" in rv.data
