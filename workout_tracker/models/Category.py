from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from . import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    exercises = relationship("Exercise", back_populates="category")
