"""Core models."""

from sqlalchemy import Column, TEXT, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Data(Base):
    """Data class."""

    __tablename__ = "data"
    # __table_args__ = {"schema": "private"}

    id = Column(TEXT, primary_key=True, nullable=False)
    created_utc = Column(TIMESTAMP(timezone=False), nullable=False)
    updated_utc = Column(TIMESTAMP(timezone=False), nullable=False)
    value = Column(TEXT, nullable=False)

    def __repr__(self):
        return "Data<value={}>".format(self.value)
