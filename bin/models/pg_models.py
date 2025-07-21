from sqlite3.dbapi2 import Timestamp
import uuid
from sqlalchemy.orm import deferred, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Column, DateTime, func, ForeignKey
from sqlalchemy import JSON, TEXT, Column, DateTime, String, Date, func , Integer,Float,Boolean
from bin.db.postgresDB import Base,engine

JSONVariant = JSON().with_variant(JSONB(), "postgresql")

def short_uuid():
    return uuid.uuid4().hex[:10]

class Timestamp:
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class User(Base,Timestamp):
    __tablename__ = "user"

    user_id = Column(String(16), default=short_uuid, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    email = Column(TEXT, unique=True, nullable=False)
    phone_number = Column(String(10), nullable=False)
    password = deferred(Column(TEXT, nullable=False))  # Deferred for security
    email_verified = Column(Boolean, nullable=False, default=False)  # Set default to False
    role_id = Column(Integer , ForeignKey("user_roles.id"), nullable=False)

class UserRole(Base,Timestamp):
    __tablename__ = "user_roles"

    id = Column(Integer , primary_key=True, index=True)
    role_name = Column(String(50), nullable=False)
