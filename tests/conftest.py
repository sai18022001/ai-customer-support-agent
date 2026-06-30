import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import Base, get_db
from app.main import app
from app.models.customer import Customer
from app.models.product import Product
from app.models.order import Order

TEST_DB_URL = "sqlite:///./test_agent.db"
test_engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestSession = sessionmaker(bind=test_engine, autoflush=False)

API_KEY = "dev-api-key-123"
HEADERS = {"X-API-Key": API_KEY}

CUSTOMER_ID = "test-cust-0001"
PRODUCT_ID = "test-prod-0001"
ORDER_ID = "test-order-0001"


def override_get_db():
    db = TestSession()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=test_engine)
    db = TestSession()

    if not db.query(Customer).filter(Customer.id == CUSTOMER_ID).first():
        db.add(Customer(
            id=CUSTOMER_ID,
            name="Test User",
            email="test@example.com",
            tier="premium",
            company="TestCorp",
        ))
        db.add(Product(
            id=PRODUCT_ID,
            name="Test Product",
            category="Testing",
            price=49.99,
            description="A test product",
        ))
        db.add(Order(
            id=ORDER_ID,
            customer_id=CUSTOMER_ID,
            product_id=PRODUCT_ID,
            quantity=2,
            total_amount=99.98,
            status="delivered",
        ))
        db.commit()

    db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def client():
    return TestClient(app)
