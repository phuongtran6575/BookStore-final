from sqlmodel import Session, select
from uuid import UUID
from models import Categories
from schema.category_schema import CategoryCreate, CategoryRead, CategoryUpdate


async def create_category(session: Session, category: CategoryCreate):
    db_category = Categories(**category.model_dump())
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category


async def get_category_by_id(session: Session, category_id: UUID):
    statement = select(Categories).where(Categories.id == category_id)
    category = session.exec(statement).first()
    return category


async def get_all_categories(session: Session) -> list[CategoryRead]:
    statement = select(Categories)
    categories = session.exec(statement).all()
    return categories


async def update_category(session: Session, category_id: UUID, category: CategoryUpdate):
    db_category = session.get(Categories, category_id)
    if not db_category:
        return None
    for key, value in category.model_dump(exclude_unset=True).items():
        setattr(db_category, key, value)
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category


def delete_category(session: Session, category_id: UUID):
    db_category = session.get(Categories, category_id)
    if not db_category:
        return False
    session.delete(db_category)
    session.commit()
    return {"status": "delete sucessful"}
