from sqlite3.dbapi2 import Timestamp
import uuid
from sqlalchemy.orm import deferred, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Column, DateTime, func, ForeignKey, UniqueConstraint
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
    full_name = Column(String(255), nullable=True)
    address = Column(String(255), nullable=True)
    email = Column(TEXT, unique=True, nullable=False)
    phone_number = Column(String(10), nullable=True)
    password = deferred(Column(TEXT, nullable=False))  # Deferred for security
    email_verified = Column(Boolean, nullable=False, default=False)  # Set default to False
    role_id = Column(Integer , ForeignKey("user_roles.id"), nullable=False)
    is_admin_approved = Column(String(16), index=True)

class UserRole(Base,Timestamp):
    __tablename__ = "user_roles"

    id = Column(Integer , primary_key=True, index=True)
    role_name = Column(String(50), nullable=False)

class Permission(Base, Timestamp):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    module_name = Column(String(100), nullable=False, unique=True)  # e.g., Events, Sermons

class RolePermission(Base, Timestamp):
    __tablename__ = "role_permissions"

    id = Column(Integer, primary_key=True)
    role_id = Column(Integer, ForeignKey("user_roles.id"), nullable=False)
    permission_id = Column(Integer, ForeignKey("permissions.id"), nullable=False)

    can_view = Column(Boolean, default=False)
    can_edit = Column(Boolean, default=False)

    __table_args__ = (UniqueConstraint("role_id", "permission_id", name="uix_role_permission"),)

class UserPermission(Base, Timestamp):  #Custom permission
    __tablename__ = "user_permissions"

    id = Column(Integer, primary_key=True)
    user_id = Column(String(16), ForeignKey("user.user_id"), nullable=False)
    permission_id = Column(Integer, ForeignKey("permissions.id"), nullable=False)

    can_view = Column(Boolean, default=False)
    can_edit = Column(Boolean, default=False)

    __table_args__ = (UniqueConstraint("user_id", "permission_id", name="uix_user_permission"),)