from typing import Type, TypeVar, List, Optional
from uuid import UUID
from sqlmodel import SQLModel, Session, select
from pydantic import BaseModel

# Generic type
ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


async def create_item( session: Session, model: type[ModelType], schema: CreateSchemaType) -> ModelType:
    obj = model(**schema.model_dump())
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj


async def get_item_by_id(session: Session,model: type[ModelType],id: UUID) -> Optional[ModelType]:
    return session.get(model, id)


async def get_list_items(session: Session, model: type[ModelType]) -> List[ModelType]:
    statement = select(model)
    result = session.exec(statement).all()
    return list(result)  


async def update_item_by_id(session: Session,model: type[ModelType], id: UUID,schema: BaseModel) -> Optional[ModelType]:
    db_obj = session.get(model, id)
    if not db_obj:
        return None

    data = schema.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(db_obj, key, value)

    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj



async def delete_item_by_id(session: Session, model: type[ModelType],id: UUID) -> bool:
    db_obj = session.get(model, id)
    if not db_obj:
        return False
    session.delete(db_obj)
    session.commit()
    return True