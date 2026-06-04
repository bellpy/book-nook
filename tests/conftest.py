import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from booknook import create_app
from booknook.db import init_db

TEST_DB = "postgresql://oscar: @localhost:5432/booknook_test"


@pytest.fixture
def app():
    app = create_app({
        "TESTING": True,
        "DATABASE_URL": TEST_DB,
    })

    with app.app_context():
        init_db()

    yield app

@pytest.fixture
def client(app):
    return app.test_client()