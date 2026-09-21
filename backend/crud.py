from typing import Sequence
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from .models.models import User, Tie, Tail, Tale, TieType


class UserRepository:
    @staticmethod
    async def create(session: AsyncSession, hashed_token: str) -> User:
        user = User(hashed_token=hashed_token)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    @staticmethod
    async def get(session: AsyncSession, hashed_token: str) -> User:
        user = await session.scalar(
            select(User)
            .where(User.hashed_token == hashed_token)
            .options(selectinload(User.ties))
        )
        return user


class TieRepository:
    @staticmethod
    async def create(session: AsyncSession, desc: str, tie_type: TieType, user_id: int) -> Tie:
        new_tie = Tie(desc=desc, type=tie_type, user_id=user_id)
        session.add(new_tie)
        await session.commit()
        await session.refresh(new_tie)
        return new_tie

    @staticmethod
    async def tie(session: AsyncSession, tie_id: int, user_id: int) -> Tie:
        tie = await session.scalar(
            select(Tie)
            .where(Tie.id == tie_id)
            .where(Tie.user_id == user_id)
            .options(selectinload(Tie.tails))
        )
        return tie

    @staticmethod
    async def ties(session: AsyncSession, user_id: int) -> Sequence[Tie]:
        ties = await session.scalars(
            select(Tie)
            .where(Tie.user_id == user_id)
        )
        return ties.all()

    @staticmethod
    async def update(session: AsyncSession, tie_id: int, desc: str, tie_type: TieType, user_id: int) -> Tie:
        tie = await TieRepository.tie(session, tie_id, user_id)
        if tie:
            if desc:
                tie.desc = desc
            if tie_type:
                tie.type = tie_type
            await session.commit()
            await session.refresh(tie)
        return tie

    @staticmethod
    async def delete(session: AsyncSession, tie_id: int, user_id: int) -> Tie:
        tie = await TieRepository.tie(session, tie_id, user_id)
        if tie:
            await session.delete(tie)
            await session.commit()
            return tie
        else:
            raise HTTPException(status_code=400, detail="Нет такой связки!")


class TailRepository:
    @staticmethod
    async def create(session: AsyncSession, desc: str, tie_id: int, user_id: int) -> Tail:
        tie = await session.get(Tie, tie_id)
        if tie and tie.user_id == user_id:
            new_tail = Tail(desc=desc, tie_id=tie_id)
            session.add(new_tail)
            await session.commit()
            await session.refresh(new_tail)
        else:
            raise HTTPException(status_code=400)
        return new_tail

    @staticmethod
    async def tail(session: AsyncSession, tail_id: int, user_id: int) -> Tail:
        # комбо с джойном и оберткой в scalar для краткости
        tail = await session.scalar(
            select(Tail)
            .join(Tie, Tail.tie_id==Tie.id)
            .where(Tie.user_id==user_id)
            .where(Tail.id==tail_id)
            .options(selectinload(Tail.tales))
        )
        return tail

    @staticmethod
    async def tails(session: AsyncSession, tie_id: int, user_id: int) -> Sequence[Tail]:
        tails = await session.scalars(
            select(Tail)
            .join(Tie, Tail.tie_id==Tie.id)
            .where(Tie.user_id==user_id)
            .where(Tail.tie_id == tie_id)
            .options(selectinload(Tail.tales))
        )
        return tails.all()

    @staticmethod
    async def update(session: AsyncSession, tail_id: int, user_id: int, desc: str | None = None, status: str | None = None) -> Tail:
        tail = await TailRepository.tail(session, tail_id, user_id)
        if not tail:
            return None
        if desc:
            tail.desc = desc
        if status:
            tail.status = status
        #
        await session.commit()
        await session.refresh(tail)
        return tail

    @staticmethod
    async def delete(session: AsyncSession, tail_id: int, user_id: int) -> Tail:
        # комбо с джойном и оберткой в scalar для краткости
        tail = await TailRepository.tail(session, tail_id, user_id)
        if tail:
            await session.delete(tail)
            await session.commit()
            return tail
        else:
            raise HTTPException(status_code=400, detail="У пользователя нет такого хвоста!")  # detail можно переопределить


class TaleRepository:
    @staticmethod
    async def create(session: AsyncSession, desc: str, tail_id: int, user_id: int) -> Tale:
        tail = await TailRepository.tail(session, tail_id, user_id)
        if tail and tail.tie.user_id == user_id:
            new_tale = Tale(desc=desc, tail_id=tail_id)
            session.add(new_tale)
            await session.commit()
            await session.refresh(new_tale)
            return new_tale
        else:
            raise HTTPException(status_code=400)

    @staticmethod
    async def tale(session: AsyncSession, tale_id: int, user_id: int) -> Tale:
        # комбо с джойном и оберткой в scalar для краткости
        tale = await session.scalar(
            select(Tale)
            .join(Tail, Tale.tail_id==Tail.id)
            .join(Tie, Tail.tie_id==Tie.id)
            .where(Tie.user_id==user_id)
            .where(Tale.id==tale_id)
        )
        return tale

    @staticmethod
    async def update(session: AsyncSession, tale_id: int, desc: str, user_id: int) -> Tale:
        tale = await TaleRepository.tale(session, tale_id, user_id)
        if tale:
            tale.desc = desc
            await session.commit()
            await session.refresh(tale)
        return tale

    @staticmethod
    async def delete(session: AsyncSession, tale_id: int, user_id: int) -> Tale:
        tale = await TaleRepository.tale(session, tale_id, user_id)
        if tale:
            await session.delete(tale)
            await session.commit()
            return tale
        else:
            raise HTTPException(status_code=400)
