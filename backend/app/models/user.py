"""
User model for the actuarial exam prep platform.
"""
from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import String, Boolean, Index
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, IdMixin, TimestampMixin


class UserRole(str, Enum):
    """Enum for user roles."""
    STUDENT = "student"
    ADMIN = "admin"
    CONTENT_CREATOR = "content_creator"


class User(Base, IdMixin, TimestampMixin):
    """User model for authentication and profile management."""

    __tablename__ = "users"
    __table_args__ = (
        Index("ix_users_email", "email", unique=True),
    )

    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    role: Mapped[UserRole] = mapped_column(
        default=UserRole.STUDENT,
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email}, full_name={self.full_name}, role={self.role})>"
