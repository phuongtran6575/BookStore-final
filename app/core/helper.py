from uuid import UUID

from models import Categories
from schema.category_schema import CategoryRead

def to_uuid(val: str | UUID) -> UUID:
    """Convert string or UUID to UUID object."""
    if isinstance(val, UUID):
        return val
    return UUID(val)  #

def to_category_read(category: Categories) -> CategoryRead:
    return CategoryRead(
        id=category.id,
        name=category.name,
        slug=category.slug,
        parentName=category.parent.name if category.parent else None,
    )