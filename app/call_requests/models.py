from typing import Optional
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base, int_pk, created_at


class CallRequest(Base):
    id: Mapped[int_pk]
    created_at: Mapped[created_at]
    fio: Mapped[str]
    phone_number: Mapped[str]
    comment: Mapped[str | None] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String, default='new', nullable=False)


    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, "
                f"created_at={self.created_at!r},"
                f"fio={self.fio!r},"
                f"phone_number={self.phone_number!r},"
                f"comment={self.comment!r},"
                f"status={self.status!r})")

    def __repr__(self):
        return str(self)
    
    def to_dict(self):
        return {
            "id": self.id,
            "created_at": self.created_at,
            "fio": self.fio,
            "phone_number": self.phone_number,
            "comment": self.comment,
            "status": self.status
        } 