from sqlmodel import Session, select
from uuid import UUID
from models import Categories
from schema.category_schema import CategoryCreate, CategoryRead, CategoryUpdate


def create_category(session: Session, category: CategoryCreate) -> CategoryRead:
    db_category = Categories(**category.dict())
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return CategoryRead.from_orm(db_category)


def get_category(session: Session, category_id: UUID) -> CategoryRead | None:
    statement = select(Categories).where(Categories.id == category_id)
    result = session.exec(statement).first()
    return CategoryRead.from_orm(result) if result else None


def list_categories(session: Session) -> list[CategoryRead]:
    statement = select(Categories)
    results = session.exec(statement).all()
    return [CategoryRead.from_orm(c) for c in results]


def update_category(session: Session, category_id: UUID, category: CategoryUpdate) -> CategoryRead | None:
    db_category = session.get(Categories, category_id)
    if not db_category:
        return None
    for key, value in category.dict(exclude_unset=True).items():
        setattr(db_category, key, value)
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return CategoryRead.from_orm(db_category)


def delete_category(session: Session, category_id: UUID) -> bool:
    db_category = session.get(Categories, category_id)
    if not db_category:
        return False
    session.delete(db_category)
    session.commit()
    return True
