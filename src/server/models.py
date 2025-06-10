from typing import Optional
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass


class Repository(Base):
    __tablename__ = "repositories"
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    owner_id: Mapped[int] = mapped_column(nullable=False)
    password: Mapped[Optional[str]] = mapped_column(nullable=False)

    def __repr__(self) -> str:
        return f"Repository(id={self.id!r})"
