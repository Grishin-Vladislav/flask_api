import datetime

from sqlalchemy import create_engine, String, DateTime, func, ForeignKey
from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column, \
    Mapped, relationship

from config import *

DSN = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DSN)
Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] \
        = mapped_column(String(50), unique=True, index=True, nullable=False)
    email: Mapped[str] \
        = mapped_column(String(50), unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(String(90), nullable=False)
    salt: Mapped[str] = mapped_column(String(90), nullable=False)
    registration_time: Mapped[datetime.datetime] \
        = mapped_column(DateTime, server_default=func.now())

    adverts: Mapped[list['Advert']] = relationship(back_populates='author')

    @property
    def dict(self):
        return {
            'name': self.name,
            'email': self.email,
            'registration_time': self.registration_time.isoformat()
        }


class Advert(Base):
    __tablename__ = "adverts"
    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] \
        = mapped_column(ForeignKey('users.id', ondelete='SET NULL'),
                        nullable=True)
    name: Mapped[str] \
        = mapped_column(String(50), unique=True, index=True, nullable=False)
    description: Mapped[str] \
        = mapped_column(String(300), nullable=False)
    created_at: Mapped[datetime.datetime] \
        = mapped_column(DateTime, server_default=func.now())
    edited_at: Mapped[datetime.datetime] \
        = mapped_column(DateTime,
                        onupdate=func.now(), server_default=func.now())

    author: Mapped["User"] = relationship(back_populates='adverts')

    @property
    def dict(self):
        return {
            'name': self.name,
            'author_name': self.author.name if self.author else "deleted user",
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'edited_at': self.edited_at.isoformat()
        }


Base.metadata.create_all(bind=engine)
