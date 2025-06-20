from app.database import Base, int_pk
from sqlalchemy import Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
import decimal


class Service(Base):
    id: Mapped[int_pk]
    name: Mapped[str]
    price: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 2))
    description: Mapped[str]
    time_to_complete: Mapped[float]

    requests = relationship("RequestService", back_populates="service")

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, "
                f"name={self.name!r},"
                f"price={self.price!r},"
                f"description={self.description!r},"
                f"time_to_complete={self.time_to_complete!r})")

    def __repr__(self):
        return str(self)
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "description": self.description,
            "time_to_complete": self.time_to_complete
        }