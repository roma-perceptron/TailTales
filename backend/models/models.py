import enum
from backend.db import Base
from datetime import datetime
from typing import List, Optional
from sqlalchemy import String, DateTime, Enum, ForeignKey, func, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship


class TieType(enum.Enum):
    base = "base"
    work = "work"
    life = "life"
    # TODO фактически не используется сейчас, не понятно нужны ли вообще эти типы


class TailStatus(enum.Enum):
    new = "new"
    active = "active"
    paused = "paused"
    staged = "staged"
    pending = "pending"
    closed = "closed"
    canceled = "canceled"

class TailStatusInterface(enum.Enum):
    new = "Новая"
    active = "В работе"
    staged = "Этап завершен"
    pending = "В ожидании"
    paused = "На паузе"
    closed = "Сделано"
    canceled = "Отменено"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    hashed_token: Mapped[Optional[str]] = mapped_column(String(64), unique=True, nullable=True)
    settings: Mapped[dict] = mapped_column(JSON, default=dict)
    last_activity: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), server_onupdate=func.now())
    #
    ties: Mapped[list["Tie"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    @property
    def ties_dict(self) -> dict:
        return {tie.id: tie for tie in self.ties}


class Tie(Base):
    __tablename__ = "ties"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    desc: Mapped[str] = mapped_column(String(255))
    created: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    type: Mapped[TieType] = mapped_column(Enum(TieType), default=TieType.base, server_default="base")
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE")) # внешний ключ на юзера
    #
    user: Mapped["User"] = relationship(back_populates="ties")
    tails: Mapped[list["Tail"]] = relationship(back_populates="tie", cascade="all, delete-orphan")


class Tail(Base):
    __tablename__ = "tails"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    desc: Mapped[str] = mapped_column(String(255))
    created: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    status: Mapped[TailStatus] = mapped_column(Enum(TailStatus), default=TailStatus.new, server_default="new")
    tie_id: Mapped[int] = mapped_column(ForeignKey("ties.id", ondelete="CASCADE")) # внешний ключ на связку
    #
    tie: Mapped["Tie"] = relationship(back_populates="tails")
    tales: Mapped[list["Tale"]] = relationship(back_populates="tail", cascade="all, delete-orphan")


class Tale(Base):
    __tablename__ = "tales"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    desc: Mapped[str] = mapped_column(String(255))
    created: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    tail_id: Mapped[int] = mapped_column(ForeignKey("tails.id", ondelete="CASCADE")) # внешний ключ на хвост
    #
    tail: Mapped["Tail"] = relationship(back_populates="tales")
