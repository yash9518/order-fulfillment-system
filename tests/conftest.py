import os
import sys
import pytest

# Add project root directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Set environment variables for testing before importing app modules
os.environ["SECRET_KEY"] = "test_environment_secret_key_mock_12345"
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

from app.database import Base, engine

@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    # Create all tables in the test database
    Base.metadata.create_all(bind=engine)
    yield
    # Drop tables after test session completes
    Base.metadata.drop_all(bind=engine)
    if os.path.exists("test.db"):
        try:
            os.remove("test.db")
        except OSError:
            pass