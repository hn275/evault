from datetime import datetime, timezone
from sqlalchemy import ForeignKey, String, Integer, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=True)

    # Relationships
    repositories = relationship(
        "Repository", back_populates="owner", cascade="all, delete-orphan"
    )
    env_created = relationship(
        "Env", back_populates="creator", cascade="all, delete-orphan"
    )
    versions_created = relationship(
        "Version", back_populates="creator", cascade="all, delete-orphan"
    )


class Repository(Base):
    __tablename__ = "repositories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    bucket_addr: Mapped[str] = mapped_column(String(255), nullable=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    # Relationships
    owner = relationship("User", back_populates="repositories")
    envs = relationship(
        "Env", back_populates="repository", cascade="all, delete-orphan"
    )
    versions = relationship(
        "Version", back_populates="repository", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Repository(id={self.id!r}, name={self.name!r})"


class Version(Base):
    __tablename__ = "versions"

    id: Mapped[int] = mapped_column(primary_key=True)
    file_id: Mapped[str] = mapped_column(String(255), nullable=False)
    s3_id: Mapped[str] = mapped_column(String(255), nullable=False)
    version_number: Mapped[int] = mapped_column(default=1)
    change_description: Mapped[str] = mapped_column(String(1000))
    repository_id: Mapped[int] = mapped_column(
        ForeignKey("repositories.id"), nullable=False
    )
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now(timezone.utc)
    )
    checksum: Mapped[str] = mapped_column(String(64), nullable=False)

    # Relationships
    repository = relationship("Repository", back_populates="versions")
    creator = relationship("User", back_populates="versions_created")


class Env(Base):
    __tablename__ = "envs"

    id: Mapped[int] = mapped_column(primary_key=True)
    key: Mapped[str] = mapped_column(String(255), nullable=False)
    value: Mapped[str] = mapped_column(String(1000), nullable=False)
    stage: Mapped[str] = mapped_column(String(50), nullable=False)
    repository_id: Mapped[int] = mapped_column(
        ForeignKey("repositories.id"), nullable=False
    )
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now(timezone.utc)
    )

    # Relationships
    repository = relationship("Repository", back_populates="envs")
    creator = relationship("User", back_populates="env_created")
