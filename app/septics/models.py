from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base, int_pk


class Septic(Base):
    id: Mapped[int_pk]
    city: Mapped[str]
    street: Mapped[str]
    house: Mapped[str]
    volume: Mapped[int]
    model: Mapped[str]
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="septics")
    requests = relationship("Request", back_populates="septic")

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, "
                f"city={self.city!r},"
                f"street={self.street!r},"
                f"house={self.house!r},"
                f"volume={self.volume!r},"
                f"model={self.model!r},"
                f"owner_id={self.owner_id!r})")

    def __repr__(self):
        return str(self)
    
    def to_dict(self):
        return {
            "id": self.id,
            "city": self.city,
            "street": self.street,
            "house": self.house,
            "volume": self.volume,
            "model": self.model,
            "owner_id": self.owner_id
        }