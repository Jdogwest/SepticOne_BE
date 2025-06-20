from datetime import date, time
from sqlalchemy import ForeignKey, Integer, String, text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base, int_pk, created_at


class Request(Base):
    id: Mapped[int_pk]
    created_at: Mapped[created_at]
    client_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    contract_number: Mapped[str] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String, default="new", server_default=text("'new'"))
    summary: Mapped[int] = mapped_column(Integer, default=0)
    septic_id: Mapped[int] = mapped_column(Integer, ForeignKey("septics.id"))
    planed_start_time: Mapped[time]
    planed_start_date: Mapped[date]
    comment: Mapped[str | None] = mapped_column(String, nullable=True)
    brigadier_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)


    brigadier = relationship("User", back_populates="requests_brigadier", foreign_keys='Request.brigadier_id')
    client = relationship("User", back_populates="requests", foreign_keys='Request.client_id')
    septic = relationship("Septic", back_populates="requests")
    services = relationship("RequestService", back_populates="request")

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, "
                f"created_at={self.created_at!r},"
                f"client_id={self.client_id!r},"
                f"contract_number={self.contract_number!r},"
                f"status={self.status!r},"
                f"summary={self.summary!r},"
                f"septic_id={self.septic_id!r},"
                f"planed_start_date={self.planed_start_date!r},"
                f"planed_start_time={self.planed_start_time!r})")

    def __repr__(self):
        return str(self)
    
    def to_dict(self):
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "client_id": self.client_id,
            "contract_number": self.contract_number,
            "status": self.status,
            "summary": self.summary,
            "septic_id": self.septic_id,
            "planed_start_date": self.planed_start_date.isoformat(),
            "planed_start_time": self.planed_start_time.strftime("%H:%M"),
            "comment": self.comment,

            "client": self.client.to_dict() if hasattr(self, 'client') and self.client is not None else None,
            "septic": self.septic.to_dict() if hasattr(self, 'septic') and self.septic is not None else None,

            # Обработка списка услуг
            "services": [
                {
                    "service_id": rs.service_id,
                    "amount": rs.amount,
                    "name": rs.service.name if rs.service else None
                }
                for rs in (self.services or [])
            ]
        }