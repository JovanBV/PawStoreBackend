from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, validates
from sqlalchemy import Integer, String, ForeignKey, Boolean, UniqueConstraint, Index, TIMESTAMP, func
from datetime import datetime
from typing import List

class Base(DeclarativeBase):
    pass



class Roles(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    role: Mapped[str] = mapped_column(String(30), unique=True)
    description: Mapped[str] = mapped_column(String(30))

    users_roles: Mapped[List["UsersRoles"]] = relationship(back_populates="role")

    def to_dict(self):
        return {
            "id": self.id,
            "role": self.role,
            "description": self.description
        }

    @validates('role')
    def convert_role_lower(self, key, value):
        return value.lower() if value else value

class UsersRoles(Base):
    __tablename__ = "users_roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=False)

    user: Mapped["Users"] = relationship(back_populates="users_roles")
    role: Mapped["Roles"] = relationship(back_populates="users_roles")

    __table_args__ = (
        UniqueConstraint("user_id", "role_id", name='uq_user_role'),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "role_id": self.role_id
        }   

class Addresses(Base):
    __tablename__ = "addresses"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    street_address: Mapped[str] = mapped_column(String(30), nullable=False)
    country: Mapped[str] = mapped_column(String(30), nullable=False)
    city: Mapped[str] = mapped_column(String(30), nullable=False)
    is_default: Mapped[bool] = mapped_column(Boolean(),default=False)
    postal_code: Mapped[str] = mapped_column(String(30), nullable=False)

    user: Mapped["Users"] = relationship(back_populates="addresses") 

    __table_args__ = (
        UniqueConstraint(
            "user_id", "street_address", "country", "city", "postal_code", 
            name="uq_user_complete_address"
        ),        
        Index(
            "unique_default_address_for_user",
            "user_id",
            unique=True,
            postgresql_where=(is_default == True)
        )
    )

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "street_address": self.street_address,
            "country": self.country,
            "city": self.city,
            "postal_code": self.postal_code,
            "is_default": self.is_default
        }   

class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    password: Mapped[str] = mapped_column(String(255))
    phone: Mapped[str] = mapped_column(String(30), nullable=True)
    email: Mapped[str] = mapped_column(String(30), unique=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean(), nullable=True)

    addresses: Mapped[List["Addresses"]] = relationship(back_populates="user")
    users_roles: Mapped[List["UsersRoles"]] = relationship(back_populates="user")
    shopping_carts: Mapped[List["ShoppingCarts"]] = relationship(back_populates="user")

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.name,
            "email": self.email,
            "roles": self.get_roles()
        }

    def get_roles(self) -> List[str]:
        try:
            return [user_role.role.role for user_role in self.users_roles]
        except:
            return []


class ShoppingCarts(Base):
    __tablename__ = "shopping_carts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True)
    total_amount: Mapped[int] = mapped_column(Integer(), default=0, nullable=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(), server_default=func.now(), nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean(), default=False, nullable=True)
    deletion_date: Mapped[datetime] = mapped_column(TIMESTAMP(), nullable=True)
    completed_at: Mapped[datetime] = mapped_column(TIMESTAMP(), nullable=True)

    user: Mapped["Users"] = relationship(back_populates="shopping_carts")
    cart_items: Mapped[List["CartItems"]] = relationship(back_populates="shopping_cart")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "is_active": self.is_active,
            "total_amount": self.total_amount,
            "created_at": self.created_at
        }

class Products(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    image_url: Mapped[str] = mapped_column(String(500))
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(200), nullable=False)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    stock: Mapped[int] = mapped_column(Integer(), nullable=False)
    price: Mapped[int] = mapped_column(Integer(), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=True, default=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean(), default=False)
    deleted_at: Mapped[datetime] = mapped_column(TIMESTAMP(), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "stock": self.stock,
            "is_active": self.is_active,
            "price": self.price,
            "image_url": self.image_url,
            "category": self.category,
            "description": self.description
        }

class CartItems(Base):
    __tablename__ = "cart_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    shopping_cart_id: Mapped[int] = mapped_column(ForeignKey("shopping_carts.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(Integer())
    price: Mapped[int] = mapped_column(Integer())

    shopping_cart: Mapped["ShoppingCarts"] = relationship(back_populates="cart_items")
    product: Mapped["Products"] = relationship()

    def to_dict(self):
        return {
            "id": self.id,
            "shopping_cart_id": self.shopping_cart_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "price": self.price
        }