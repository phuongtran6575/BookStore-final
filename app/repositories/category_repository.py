from sqlmodel import  Session
from models import Categories
from uuid import UUID, uuid4


async def get_category_by_id(category_id: UUID,session: Session):
    statement = select(Categories).where(Categories.id == category_id)
    category = session.exec(statement).first()
    return category

async def get_all_category(session: Session):
    statement = select(Categories)
    list_category = session.exec(statement).all()
    return list_category

async def create_category(category: Categories, session: Session):
    category_data = Categories(
        id = uuid4(),
        name = category.name
    )
    session.add(category_data)
    session.commit()
    sessin.refresh(category_data)
    return category_data

async def update_category(category_id: UUID, category: Categories ,session: Session):
    statement = select(Categories).where(Categories.id == category_id)
    category_update = session.exec(statement).first()
    if category_update:
        category_update.name = category.name
    return category_update

async def delete_category(category_id: UUID, session: Session):
    statement = select(Categories).where(Categories.id == category_id)
    category = session.exec(statement).first()
    if category:
        session.delete(category)
        session.commit()
    return {"message": "delete success"}