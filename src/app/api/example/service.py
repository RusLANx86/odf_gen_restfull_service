"""Data service."""

import uuid
import datetime

from sqlalchemy.orm.session import Session

from ...models.map import Data


def get_page(session: Session, page_offset: int, page_limit: int):
    """Get data page."""
    return session.query(Data).order_by(Data.value.desc()).limit(page_limit).offset((page_offset - 1) * page_limit)


def get_item(session: Session, id: str):
    """Get data item."""
    return session.query(Data).filter(Data.id == id).one()


def create_item(session: Session, value: str) -> str:
    """Create data item."""
    id = str(uuid.uuid4())
    now_utc = datetime.datetime.utcnow()
    data = Data(id=id, value=value, created_utc=now_utc, updated_utc=now_utc)
    session.add(data)
    return id


def update_item(session: Session, id: str, value: str):
    """Update data item."""
    now_utc = datetime.datetime.utcnow()
    session.query(Data).filter(Data.id == id).update({Data.value: value, Data.updated_utc: now_utc}, synchronize_session = False)


def delete_item(session: Session, id: str):
    """Delete data item."""
    session.query(Data).filter(Data.id==id).delete()
