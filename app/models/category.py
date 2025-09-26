from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from ..db.base import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    # If user_id is NULL, this is a default category available to all users
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True, index=True)

    user = relationship("User", back_populates="categories")

    __table_args__ = (
        # Enforce unique category names per user; allow same name for different users and for defaults
        UniqueConstraint("name", "user_id", name="uq_category_name_user"),
    )
