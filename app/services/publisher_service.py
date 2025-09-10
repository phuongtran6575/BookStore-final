from sqlmodel import Session
from uuid import UUID
from schema.publisher_schema import PublisherCreate, PublisherUpdate
from repositories import publisher_repository


def create_publisher_service(session: Session, publisher: PublisherCreate):
    return publisher_repository.create_publisher(session, publisher)


def get_publisher_by_id_service(session: Session, publisher_id: UUID):
    return publisher_repository.get_publisher_by_id(session, publisher_id)


def get_all_publishers_service(session: Session):
    return publisher_repository.get_list_publishers(session)


def update_publisher_service(session: Session, publisher_id: UUID, publisher: PublisherUpdate):
    return publisher_repository.update_publisher(session, publisher_id, publisher)


def delete_publisher_service(session: Session, publisher_id: UUID):
    return publisher_repository.delete_publisher(session, publisher_id)
