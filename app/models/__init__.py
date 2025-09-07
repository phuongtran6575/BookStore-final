from models.bookstore_models import  Users, Roles, UserRoles, Authors, Publishers, Categories, Tags, Products, ProductAuthors, ProductPublishers, ProductCategories, ProductTags, ProductImages, InventoryLog,Reviews,Orders, OrderItems, Payments,Addresses,Vouchers, VoucherUsage,Posts,Carts, CartItems
all_models = [
    # Users & Roles
    "Users",
    "Roles",
    "UserRoles",

    # Authors / Publishers / Categories / Tags
    "Authors",
    "Publishers",
    "Categories",
    "Tags",

    # Products & related
    "Products",
    "ProductAuthors",
    "ProductPublishers",
    "ProductCategories",
    "ProductTags",
    "ProductImages",
    "InventoryLog",

    # Reviews
    "Reviews",

    # Orders & Payments
    "Orders",
    "OrderItems",
    "Payments",

    # Addresses
    "Addresses",

    # Vouchers
    "Vouchers",
    "VoucherUsage",

    # Posts
    "Posts",

    # Carts
    "Carts",
    "CartItems",
]