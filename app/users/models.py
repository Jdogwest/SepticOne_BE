from sqlalchemy import String, text
from sqlalchemy.orm import Mapped, relationship, mapped_column
from app.database import Base, int_pk


class User(Base):
    id: Mapped[int_pk]
    name: Mapped[str]
    surname: Mapped[str]
    patronymic: Mapped[str | None] = mapped_column(String, nullable=True)
    phone_number: Mapped[str | None] = mapped_column(String, nullable=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str]
    role: Mapped[str] = mapped_column(String, default='client', server_default=text("'client'"), nullable=False)

    septics = relationship("Septic", back_populates="owner")
    requests = relationship("Request", back_populates="client", foreign_keys='Request.client_id')
    requests_brigadier = relationship("Request", back_populates="brigadier", foreign_keys='Request.brigadier_id')



    brigadier_relations = relationship(
        "WorkmanBrigadier",
        foreign_keys="WorkmanBrigadier.brigadier_id",
        back_populates="brigadier"
    )

    workman_relations = relationship(
        "WorkmanBrigadier",
        foreign_keys="WorkmanBrigadier.workman_id",
        back_populates="workman"
    )

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, "
                f"name={self.name!r},"
                f"surname={self.surname!r},"
                f"patronymic={self.patronymic!r},"
                f"phone_number={self.phone_number!r}),"
                f"email={self.email!r}),"
                f"role={self.role!r})")

    def __repr__(self):
        return str(self)
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "patronymic": self.patronymic,
            "phone_number": self.phone_number,
            "email": self.email,
            "role": self.role
        }