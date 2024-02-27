from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship

from . import Base


class Exercise(Base):
    __tablename__ = "exercises"

    name = Column(String, nullable=False, primary_key=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    category = relationship("Category", back_populates="exercises")
