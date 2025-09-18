from sqlmodel import Session
from uuid import UUID
from repositories import tag_repository
from schema.tag_schema import TagCreate, TagRead, TagUpdate


def create_tag_service(session: Session, tag: TagCreate):
    return tag_repository.create_tag(session, tag)


def get_tag_by_id_service(session: Session, tag_id: UUID):
    return tag_repository.get_tag_by_id(session, tag_id)


def get_all_tags_service(session: Session):
    return tag_repository.get_list_tags(session)


def update_tag_service(session: Session, tag_id: UUID, tag: TagUpdate):
    return tag_repository.update_tag(session, tag_id, tag)


def delete_tag_service(session: Session, tag_id: UUID):
    return tag_repository.delete_tag(session, tag_id)