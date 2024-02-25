from sqlalchemy import Column, Float, Text, ForeignKey, Integer
from sqlalchemy.orm import relationship

from . import Base


class Set(Base):
    __tablename__ = "sets"

    id = Column(Integer, primary_key=True)
    order = Column(Integer, nullable=False)
    workout_id = Column(Integer, ForeignKey("workouts.id"))
    exercise_id = Column(Integer, ForeignKey("exercises.id"))
    reps = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)
    notes = Column(Text)

    workout = relationship("Workout", back_populates="sets")
    exercise = relationship("Exercise")
