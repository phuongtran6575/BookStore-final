from sqlmodel import Session, select
from uuid import UUID
from models import Authors
from schema.author_schema import AuthorCreate, AuthorRead, AuthorUpdate


def create_author(session: Session, author: AuthorCreate) -> AuthorRead:
    db_author = Authors(**author.dict())
    session.add(db_author)
    session.commit()
    session.refresh(db_author)
    return AuthorRead.from_orm(db_author)


def get_author(session: Session, author_id: UUID) -> AuthorRead | None:
    statement = select(Authors).where(Authors.id == author_id)
    result = session.exec(statement).first()
    return AuthorRead.from_orm(result) if result else None


def list_authors(session: Session) -> list[AuthorRead]:
    statement = select(Authors)
    results = session.exec(statement).all()
    return [AuthorRead.from_orm(author) for author in results]


def update_author(session: Session, author_id: UUID, author: AuthorUpdate) -> AuthorRead | None:
    db_author = session.get(Authors, author_id)
    if not db_author:
        return None
    for key, value in author.dict(exclude_unset=True).items():
        setattr(db_author, key, value)
    session.add(db_author)
    session.commit()
    session.refresh(db_author)
    return AuthorRead.from_orm(db_author)


def delete_author(session: Session, author_id: UUID) -> bool:
    db_author = session.get(Authors, author_id)
    if not db_author:
        return False
    session.delete(db_author)
    session.commit()
    return True
