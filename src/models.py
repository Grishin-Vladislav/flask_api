import datetime

from sqlalchemy import create_engine, String, DateTime, func
from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column, \
    Mapped

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
    name: Mapped[str] \
        = mapped_column(String(50), unique=True, index=True, nullable=False)
    description: Mapped[str] \
        = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime.datetime] \
        = mapped_column(DateTime, server_default=func.now())
    edited_at: Mapped[datetime.datetime] \
        = mapped_column(DateTime, onupdate=func.now())


Base.metadata.create_all(bind=engine)
