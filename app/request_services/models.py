from datetime import date, datetime
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base, int_pk


class RequestService(Base):
    service_id: Mapped[int] = mapped_column(Integer, ForeignKey("services.id"), primary_key=True)
    request_id: Mapped[int] = mapped_column(Integer, ForeignKey("requests.id"), primary_key=True)
    amount: Mapped[int]

    service = relationship("Service", back_populates="requests")
    request = relationship("Request", back_populates="services")

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, "
                f"service_id={self.service_id!r},"
                f"amount={self.amount!r})")

    def __repr__(self):
        return str(self)
    
    def to_dict(self):
        return {
            "id": self.id,
            "service_id": self.service_id,
            "amount": self.amount
        }