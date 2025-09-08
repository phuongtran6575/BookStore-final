from sqlmodel import Session, select
from uuid import UUID
from models import Tags
from schema.tag_schema import TagCreate, TagRead, TagUpdate


def create_tag(session: Session, tag: TagCreate):
    db_tag = Tags(**tag.dict())
    session.add(db_tag)
    session.commit()
    session.refresh(db_tag)
    return db_tag


def get_tag(session: Session, tag_id: UUID):
    statement = select(Tags).where(Tags.id == tag_id)
    tag = session.exec(statement).first()
    return tag


def list_tags(session: Session) -> list[TagRead]:
    statement = select(Tags)
    results = session.exec(statement).all()
    return [TagRead.from_orm(t) for t in results]


def update_tag(session: Session, tag_id: UUID, tag: TagUpdate):
    db_tag = session.get(Tags, tag_id)
    if not db_tag:
        return None
    for key, value in tag.dict(exclude_unset=True).items():
        setattr(db_tag, key, value)
    session.add(db_tag)
    session.commit()
    session.refresh(db_tag)
    return TagRead.from_orm(db_tag)


def delete_tag(session: Session, tag_id: UUID):
    db_tag = session.get(Tags, tag_id)
    if not db_tag:
        return False
    session.delete(db_tag)
    session.commit()
    return True
