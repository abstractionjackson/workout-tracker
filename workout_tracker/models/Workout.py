from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from . import Base


class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", lazy="select")
    sets = relationship(
        "Set", back_populates="workout", order_by="Set.order", lazy="select"
    )

    def get_exercises(self):
        exercises = []
        for s in self.sets:
            if s.exercise not in exercises:
                exercises.append(s.exercise)
        return exercises
