from datetime import datetime, date
from typing import Optional, List
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship

from schema.order_schema import OrderStatus, PaymentMethod, ShippingMethod


# =========================
# USERS & ROLES
# =========================

class Users(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    full_name: str
    email: str = Field(index=True, unique=True)
    password_hash: str
    phone_number: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    roles: List["UserRoles"] = Relationship(back_populates="user", cascade_delete=True)
    reviews: List["Reviews"] = Relationship(back_populates="user", cascade_delete=True)
    orders: List["Orders"] = Relationship(back_populates="user", cascade_delete=True)
    addresses: List["Addresses"] = Relationship(back_populates="user", cascade_delete=True)
    posts: List["Posts"] = Relationship(back_populates="user", cascade_delete=True)
    carts: List["Carts"] = Relationship(back_populates="user", cascade_delete=True)


class Roles(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(unique=True)

    users: List["UserRoles"] = Relationship(back_populates="role", cascade_delete=True)


class UserRoles(SQLModel, table=True):
    user_id: UUID = Field(foreign_key="users.id", primary_key=True, ondelete="CASCADE")
    role_id: UUID = Field(foreign_key="roles.id", primary_key=True, ondelete="CASCADE")

    user: Optional[Users] = Relationship(back_populates="roles")
    role: Optional[Roles] = Relationship(back_populates="users")


# =========================
# AUTHORS, PUBLISHERS, CATEGORIES, TAGS
# =========================

class Authors(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(unique=True)
    bio: Optional[str] = None

    products: List["ProductAuthors"] = Relationship(back_populates="author", cascade_delete=True)


class Publishers(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(unique=True)
    address: Optional[str] = None

    products: List["ProductPublishers"] = Relationship(back_populates="publisher", cascade_delete=True)


class Categories(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    slug: str = Field(unique=True, index=True)
    parent_id: Optional[UUID] = Field(default=None, foreign_key="categories.id")

    products: List["ProductCategories"] = Relationship(back_populates="category", cascade_delete=True)
    parent: Optional["Categories"] = Relationship(
        back_populates="children",
        sa_relationship_kwargs={"remote_side": "Categories.id"},
    )
    children: List["Categories"] = Relationship(back_populates="parent")


class Tags(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    slug: str = Field(unique=True, index=True)

    products: List["ProductTags"] = Relationship(back_populates="tag", cascade_delete=True)


# =========================
# PRODUCTS & RELATED TABLES
# =========================

class Products(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str
    description: Optional[str] = None
    sku: str = Field(unique=True, index=True)
    size: Optional[str] = Field(default= None)
    price: float
    sale_price: Optional[float] = None
    stock_quantity: int = Field(default=0)
    page_count: Optional[int] = None
    cover_type: Optional[str] = None
    publication_date: Optional[date] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    authors: List["ProductAuthors"] = Relationship(back_populates="product", cascade_delete=True)
    publishers: List["ProductPublishers"] = Relationship(back_populates="product", cascade_delete=True)
    categories: List["ProductCategories"] = Relationship(back_populates="product",cascade_delete=True)
    tags: List["ProductTags"] = Relationship(back_populates="product", cascade_delete=True)
    images: List["ProductImages"] = Relationship(back_populates="product", cascade_delete=True)
    reviews: List["Reviews"] = Relationship(back_populates="product", cascade_delete=True)
    order_items: List["OrderItems"] = Relationship(back_populates="product", cascade_delete=True)
    cart_items: List["CartItems"] = Relationship(back_populates="product",cascade_delete=True)
    inventory_logs: List["InventoryLog"] = Relationship(back_populates="product",cascade_delete=True)


class ProductAuthors(SQLModel, table=True):
    product_id: UUID = Field(foreign_key="products.id", primary_key=True, ondelete="CASCADE")
    author_id: UUID = Field(foreign_key="authors.id", primary_key=True, ondelete="CASCADE")

    product: Optional[Products] = Relationship(back_populates="authors")
    author: Optional[Authors] = Relationship(back_populates="products")


class ProductPublishers(SQLModel, table=True):
    product_id: UUID = Field(foreign_key="products.id", primary_key=True, ondelete="CASCADE")
    publisher_id: UUID = Field(foreign_key="publishers.id", primary_key=True, ondelete="CASCADE")
    edition: Optional[str] = None
    year: Optional[int] = None
    isbn: Optional[str] = None

    product: Products = Relationship(back_populates="publishers")
    publisher: Publishers = Relationship(back_populates="products")


class ProductCategories(SQLModel, table=True):
    product_id: UUID = Field(foreign_key="products.id", primary_key=True, ondelete="CASCADE")
    category_id: UUID = Field(foreign_key="categories.id", primary_key=True, ondelete="CASCADE")

    product: Optional[Products] = Relationship(back_populates="categories")
    category: Optional[Categories] = Relationship(back_populates="products")


class ProductTags(SQLModel, table=True):
    product_id: UUID = Field(foreign_key="products.id", primary_key=True, ondelete="CASCADE")
    tag_id: UUID = Field(foreign_key="tags.id", primary_key=True, ondelete="CASCADE")

    product: Optional[Products] = Relationship(back_populates="tags")
    tag: Optional[Tags] = Relationship(back_populates="products")


class ProductImages(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    product_id: UUID = Field(foreign_key="products.id", ondelete="CASCADE")
    image_url: str
    is_thumbnail: bool = Field(default=False)

    product: Optional[Products] = Relationship(back_populates="images")


class InventoryLog(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    product_id: UUID = Field(foreign_key="products.id", ondelete="CASCADE")
    change_type: str  # import, export, adjust
    quantity_change: int
    created_at: datetime = Field(default_factory=datetime.utcnow)
    note: Optional[str] = None

    product: Optional[Products] = Relationship(back_populates="inventory_logs")


# =========================
# REVIEWS
# =========================

class Reviews(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    product_id: UUID = Field(foreign_key="products.id", ondelete="CASCADE")
    user_id: UUID = Field(foreign_key="users.id", ondelete="CASCADE")
    rating: int
    comment: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    product: Optional[Products] = Relationship(back_populates="reviews")
    user: Optional[Users] = Relationship(back_populates="reviews")


# =========================
# ORDERS
# =========================

class Orders(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: Optional[UUID] = Field(default=None, foreign_key="users.id", ondelete="CASCADE")
    customer_name: str
    customer_email: str
    customer_phone: str
    shipping_address: str
    total_amount: float
    status: OrderStatus = Field(default=OrderStatus.PENDING)  # ✅ Enum
    payment_method: PaymentMethod
    shipping_method: ShippingMethod
    created_at: datetime = Field(default_factory=datetime.utcnow)

    user: Optional[Users] = Relationship(back_populates="orders")
    items: List["OrderItems"] = Relationship(back_populates="order")
    payments: List["Payments"] = Relationship(back_populates="order")


class OrderItems(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    order_id: UUID = Field(foreign_key="orders.id", ondelete="CASCADE")
    product_id: UUID = Field(foreign_key="products.id", ondelete="CASCADE")
    image_url: str
    quantity: int
    price: float  # snapshot price
    subtotal: float

    order: Optional[Orders] = Relationship(back_populates="items")
    product: Optional[Products] = Relationship(back_populates="order_items")


class Payments(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    order_id: UUID = Field(foreign_key="orders.id", ondelete="CASCADE")
    transaction_id: Optional[str] = None
    amount: float
    status: str  # pending, paid, failed, refunded
    method: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    order: Optional[Orders] = Relationship(back_populates="payments")


# =========================
# ADDRESSES
# =========================

class Addresses(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", ondelete="CASCADE")
    phone_number: str
    full_name:str
    full_address: str
    is_default: bool = Field(default=False)

    user: Optional[Users] = Relationship(back_populates="addresses")


# =========================
# VOUCHERS
# =========================

class Vouchers(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    code: str = Field(unique=True, index=True)
    type: str  # fixed, percentage
    value: float
    quantity: int
    min_order_value: Optional[float] = None
    start_date: datetime
    end_date: datetime
    max_discount: Optional[float] = None

    usage: List["VoucherUsage"] = Relationship(back_populates="voucher")


class VoucherUsage(SQLModel, table=True):
    voucher_id: UUID = Field(foreign_key="vouchers.id", primary_key=True, ondelete="CASCADE")
    user_id: UUID = Field(foreign_key="users.id", primary_key=True, ondelete="CASCADE")
    order_id: UUID = Field(foreign_key="orders.id", ondelete="CASCADE")
    used_at: datetime = Field(default_factory=datetime.utcnow)

    voucher: Optional[Vouchers] = Relationship(back_populates="usage")


# =========================
# POSTS (BLOG / NEWS)
# =========================

class Posts(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id")  # must be admin (app logic)
    title: str
    slug: str = Field(unique=True, index=True)
    content: str
    thumbnail_url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    user: Optional[Users] = Relationship(back_populates="posts")


# =========================
# CARTS
# =========================

class Carts(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: Optional[UUID] = Field(default=None, foreign_key="users.id")
    session_id: Optional[str] = Field(default=None, unique=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    user: Optional[Users] = Relationship(back_populates="carts")
    items: List["CartItems"] = Relationship(back_populates="cart")


class CartItems(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    cart_id: UUID = Field(foreign_key="carts.id")
    product_id: UUID = Field(foreign_key="products.id")
    quantity: int = Field(default=1)
    added_at: datetime = Field(default_factory=datetime.utcnow)

    cart: Optional[Carts] = Relationship(back_populates="items")
    product: Optional[Products] = Relationship(back_populates="cart_items")
