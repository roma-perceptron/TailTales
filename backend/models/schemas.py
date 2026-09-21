from pydantic import BaseModel
from backend.models.models import TieType, TailStatus


class UserCreate(BaseModel):
    hashed_token: str

class TieCreate(BaseModel):
    desc: str
    tie_type: TieType

class TieUpdate(BaseModel):
    tie_id: int
    desc: str | None
    tie_type: TieType | None

class TieDelete(BaseModel):
    tie_id: int

class TailCreate(BaseModel):
    tie_id: int
    desc: str

class TailUpdate(BaseModel):
    tail_id: int
    desc: str | None
    status: TailStatus | None

class TailDelete(BaseModel):
    tail_id: int

class TaleCreate(BaseModel):
    tail_id: int
    desc: str

class TaleUpdate(BaseModel):
    tale_id: int
    desc: str

class TokenResponse(BaseModel):
    token: str
    message: str

class TokenRequest(BaseModel):
    token: str


# схемы для использования в тестах
class FakeTale(BaseModel):
    desc: str

class FakeTail(BaseModel):
    desc: str
    tales: list[FakeTale]

class FakeTie(BaseModel):
    desc: str
    type: TieType
    tails: list[FakeTail]

class FakeUser(BaseModel):
    hashed_token: str
    ties: list[FakeTie]
    id: int | None = None
