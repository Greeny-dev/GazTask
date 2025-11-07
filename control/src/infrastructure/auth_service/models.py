"""
Obviously, no database queries should be made here.
This is an external service, but for the sake of emulation, this is what we have to do.
"""

from infrastructure.database import Base
from sqlalchemy import Boolean, Column, DateTime, Integer, String, func


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    is_admin = Column(Boolean, default=False)

    def __repr__(self):
        return (
            f"<User(id={self.id}, username='{self.username}', admin={self.is_admin})>"
        )
