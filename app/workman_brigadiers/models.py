from app.database import Base
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import relationship, Mapped, mapped_column


class WorkmanBrigadier(Base):
    brigadier_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
    workman_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)

    brigadier = relationship("User", foreign_keys=[brigadier_id])
    workman = relationship("User", foreign_keys=[workman_id])

    def __str__(self):
        return (f"{self.__class__.__name__}(workman_id={self.workman_id}, "
                f"brigadier_id={self.brigadier_id!r})")

    def __repr__(self):
        return str(self)
    
    def to_dict(self):
        return {
            "workman_id": self.workman_id,
            "brigadier_id": self.brigadier_id
        }