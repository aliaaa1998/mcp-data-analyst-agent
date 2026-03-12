from datetime import date

from sqlalchemy import Date, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Sales(Base):
    __tablename__ = "sales"
    order_id: Mapped[str] = mapped_column(String, primary_key=True)
    order_date: Mapped[date] = mapped_column(Date, index=True)
    product_id: Mapped[str] = mapped_column(String, index=True)
    region_id: Mapped[str] = mapped_column(String, index=True)
    customer_id: Mapped[str] = mapped_column(String, index=True)
    revenue: Mapped[float] = mapped_column(Float)
    quantity: Mapped[int] = mapped_column(Integer)
    cost: Mapped[float] = mapped_column(Float)


class Product(Base):
    __tablename__ = "products"
    product_id: Mapped[str] = mapped_column(String, primary_key=True)
    product_name: Mapped[str] = mapped_column(String)
    category: Mapped[str] = mapped_column(String)
    subcategory: Mapped[str] = mapped_column(String)
    price: Mapped[float] = mapped_column(Float)


class Customer(Base):
    __tablename__ = "customers"
    customer_id: Mapped[str] = mapped_column(String, primary_key=True)
    segment: Mapped[str] = mapped_column(String)
    country: Mapped[str] = mapped_column(String)
    signup_date: Mapped[date] = mapped_column(Date)
    churned: Mapped[bool]


class Region(Base):
    __tablename__ = "regions"
    region_id: Mapped[str] = mapped_column(String, primary_key=True)
    region_name: Mapped[str] = mapped_column(String)
    market: Mapped[str] = mapped_column(String)


class Churn(Base):
    __tablename__ = "churn"
    month: Mapped[str] = mapped_column(String, primary_key=True)
    segment: Mapped[str] = mapped_column(String, primary_key=True)
    churn_rate: Mapped[float] = mapped_column(Float)
    retained_customers: Mapped[int] = mapped_column(Integer)
