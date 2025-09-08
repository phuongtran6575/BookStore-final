from sqlmodel import Session, select
from uuid import UUID
from models import Publishers
from schema.publisher_schema import PublisherCreate, PublisherRead, PublisherUpdate


def create_publisher(session: Session, publisher: PublisherCreate) -> PublisherRead:
    db_publisher = Publishers(**publisher.dict())
    session.add(db_publisher)
    session.commit()
    session.refresh(db_publisher)
    return PublisherRead.from_orm(db_publisher)


def get_publisher(session: Session, publisher_id: UUID) -> PublisherRead | None:
    statement = select(Publishers).where(Publishers.id == publisher_id)
    result = session.exec(statement).first()
    return PublisherRead.from_orm(result) if result else None


def list_publishers(session: Session) -> list[PublisherRead]:
    statement = select(Publishers)
    results = session.exec(statement).all()
    return [PublisherRead.from_orm(p) for p in results]


def update_publisher(session: Session, publisher_id: UUID, publisher: PublisherUpdate) -> PublisherRead | None:
    db_publisher = session.get(Publishers, publisher_id)
    if not db_publisher:
        return None
    for key, value in publisher.dict(exclude_unset=True).items():
        setattr(db_publisher, key, value)
    session.add(db_publisher)
    session.commit()
    session.refresh(db_publisher)
    return PublisherRead.from_orm(db_publisher)


def delete_publisher(session: Session, publisher_id: UUID) -> bool:
    db_publisher = session.get(Publishers, publisher_id)
    if not db_publisher:
        return False
    session.delete(db_publisher)
    session.commit()
    return True
