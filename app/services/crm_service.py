from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.order import Order
from app.models.product import Product
from app.core.exceptions import NotFoundError


class CRMService:
    def __init__(self, db: Session):
        self.db = db

    # ── Customers ──

    def get_customer(self, customer_id: str) -> Customer:
        customer = self.db.query(Customer).filter(Customer.id == customer_id).first()
        if not customer:
            raise NotFoundError("Customer", customer_id)
        return customer

    def list_customers(
        self,
        tier: str | None = None,
        search: str | None = None,
        page: int = 1,
        limit: int = 20,
    ) -> list[Customer]:
        query = self.db.query(Customer)
        if tier:
            query = query.filter(Customer.tier == tier)
        if search:
            pattern = f"%{search}%"
            query = query.filter(
                Customer.name.ilike(pattern) | Customer.email.ilike(pattern)
            )
        offset = (page - 1) * limit
        return query.offset(offset).limit(limit).all()

    def create_customer(self, **kwargs) -> Customer:
        customer = Customer(**kwargs)
        self.db.add(customer)
        self.db.commit()
        self.db.refresh(customer)
        return customer

    def update_customer(self, customer_id: str, **kwargs) -> Customer:
        customer = self.get_customer(customer_id)
        for key, value in kwargs.items():
            if value is not None:
                setattr(customer, key, value)
        self.db.commit()
        self.db.refresh(customer)
        return customer

    # ── Orders ──

    def get_order(self, order_id: str) -> Order:
        order = self.db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise NotFoundError("Order", order_id)
        return order

    def list_orders(
        self,
        customer_id: str | None = None,
        status: str | None = None,
        page: int = 1,
        limit: int = 20,
    ) -> list[Order]:
        query = self.db.query(Order)
        if customer_id:
            query = query.filter(Order.customer_id == customer_id)
        if status:
            query = query.filter(Order.status == status)
        offset = (page - 1) * limit
        return query.order_by(Order.created_at.desc()).offset(offset).limit(limit).all()

    def create_order(self, customer_id: str, product_id: str, quantity: int = 1) -> Order:
        self.get_customer(customer_id)
        product = self.db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise NotFoundError("Product", product_id)

        total = product.price * quantity
        order = Order(
            customer_id=customer_id,
            product_id=product_id,
            quantity=quantity,
            total_amount=total,
        )
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order

    def update_order(self, order_id: str, **kwargs) -> Order:
        order = self.get_order(order_id)
        for key, value in kwargs.items():
            if value is not None:
                setattr(order, key, value)
        self.db.commit()
        self.db.refresh(order)
        return order

    # ── Products ──

    def list_products(self) -> list[Product]:
        return self.db.query(Product).all()

    def get_customer_summary(self, customer_id: str) -> dict:
        customer = self.get_customer(customer_id)
        orders = (
            self.db.query(Order)
            .filter(Order.customer_id == customer_id)
            .order_by(Order.created_at.desc())
            .limit(5)
            .all()
        )
        return {
            "customer_name": customer.name,
            "customer_email": customer.email,
            "customer_tier": customer.tier,
            "company": customer.company,
            "recent_orders": [
                {
                    "order_id": o.id,
                    "status": o.status,
                    "total_amount": o.total_amount,
                }
                for o in orders
            ],
        }
