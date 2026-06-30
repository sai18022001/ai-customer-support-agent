"""Populate the database with sample customers, products, and orders."""

from app.core.database import Base, engine, SessionLocal
from app.models.customer import Customer
from app.models.product import Product
from app.models.order import Order


CUSTOMERS = [
    {
        "id": "c1000001-0000-0000-0000-000000000001",
        "name": "Alice Johnson",
        "email": "alice@techcorp.com",
        "phone": "+1-555-0101",
        "tier": "enterprise",
        "company": "TechCorp Inc.",
    },
    {
        "id": "c1000001-0000-0000-0000-000000000002",
        "name": "Bob Smith",
        "email": "bob@startup.io",
        "phone": "+1-555-0102",
        "tier": "premium",
        "company": "Startup.io",
    },
    {
        "id": "c1000001-0000-0000-0000-000000000003",
        "name": "Carol Davis",
        "email": "carol@freelance.dev",
        "phone": "+1-555-0103",
        "tier": "basic",
        "company": None,
    },
    {
        "id": "c1000001-0000-0000-0000-000000000004",
        "name": "David Lee",
        "email": "david@enterprise.co",
        "phone": "+1-555-0104",
        "tier": "enterprise",
        "company": "Enterprise Co.",
    },
    {
        "id": "c1000001-0000-0000-0000-000000000005",
        "name": "Eva Martinez",
        "email": "eva@designhub.com",
        "phone": "+1-555-0105",
        "tier": "premium",
        "company": "DesignHub",
    },
]

PRODUCTS = [
    {
        "id": "p2000001-0000-0000-0000-000000000001",
        "name": "CloudSync Pro",
        "category": "SaaS Platform",
        "price": 99.99,
        "description": "Enterprise cloud synchronization platform",
    },
    {
        "id": "p2000001-0000-0000-0000-000000000002",
        "name": "DataVault Basic",
        "category": "Storage",
        "price": 29.99,
        "description": "Secure cloud storage solution",
    },
    {
        "id": "p2000001-0000-0000-0000-000000000003",
        "name": "Analytics Dashboard",
        "category": "Analytics",
        "price": 149.99,
        "description": "Real-time business analytics dashboard",
    },
    {
        "id": "p2000001-0000-0000-0000-000000000004",
        "name": "TeamFlow",
        "category": "Collaboration",
        "price": 49.99,
        "description": "Team collaboration and workflow tool",
    },
    {
        "id": "p2000001-0000-0000-0000-000000000005",
        "name": "SecureAuth Enterprise",
        "category": "Identity",
        "price": 199.99,
        "description": "Enterprise identity and access management",
    },
]

ORDERS = [
    {
        "id": "o3000001-0000-0000-0000-000000000001",
        "customer_id": "c1000001-0000-0000-0000-000000000001",
        "product_id": "p2000001-0000-0000-0000-000000000001",
        "quantity": 5,
        "total_amount": 499.95,
        "status": "delivered",
    },
    {
        "id": "o3000001-0000-0000-0000-000000000002",
        "customer_id": "c1000001-0000-0000-0000-000000000001",
        "product_id": "p2000001-0000-0000-0000-000000000005",
        "quantity": 1,
        "total_amount": 199.99,
        "status": "shipped",
    },
    {
        "id": "o3000001-0000-0000-0000-000000000003",
        "customer_id": "c1000001-0000-0000-0000-000000000002",
        "product_id": "p2000001-0000-0000-0000-000000000003",
        "quantity": 2,
        "total_amount": 299.98,
        "status": "confirmed",
    },
    {
        "id": "o3000001-0000-0000-0000-000000000004",
        "customer_id": "c1000001-0000-0000-0000-000000000003",
        "product_id": "p2000001-0000-0000-0000-000000000002",
        "quantity": 1,
        "total_amount": 29.99,
        "status": "pending",
    },
    {
        "id": "o3000001-0000-0000-0000-000000000005",
        "customer_id": "c1000001-0000-0000-0000-000000000004",
        "product_id": "p2000001-0000-0000-0000-000000000001",
        "quantity": 10,
        "total_amount": 999.90,
        "status": "delivered",
    },
    {
        "id": "o3000001-0000-0000-0000-000000000006",
        "customer_id": "c1000001-0000-0000-0000-000000000005",
        "product_id": "p2000001-0000-0000-0000-000000000004",
        "quantity": 3,
        "total_amount": 149.97,
        "status": "cancelled",
    },
]


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    if db.query(Customer).count() > 0:
        print("Database already seeded. Skipping.")
        db.close()
        return

    for c in CUSTOMERS:
        db.add(Customer(**c))
    for p in PRODUCTS:
        db.add(Product(**p))
    for o in ORDERS:
        db.add(Order(**o))

    db.commit()
    db.close()
    print(f"Seeded {len(CUSTOMERS)} customers, {len(PRODUCTS)} products, {len(ORDERS)} orders.")


if __name__ == "__main__":
    seed()
