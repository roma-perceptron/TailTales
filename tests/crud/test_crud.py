import pytest
import random
from enum import Enum
from pydantic import BaseModel
from fastapi import HTTPException
from dataclasses import dataclass
from typing import get_args, get_origin
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.schemas import FakeUser, FakeTie, FakeTail, FakeTale
from backend.models.models import User, Tie, Tail, Tale, TieType, TailStatus
from backend.crud import UserRepository, TieRepository, TailRepository, TaleRepository


"""
    CRUD методы устроены так: на вход всегда (кроме создания User) требуется user_id и при любых операциях проверяется
    связан ли новый/изменяемый объект с этим пользователем. Он может работать только со своими данными.
    Таким образом, зная use_id можно делать что угодно с любыми данными, но CRUD-методы не доступны сами по себе. Они
    обернуты в API методы, которые не принимают user_id от клиента, а сами его определяют (cookie в request) и добавляют
    к вызову CRUD-метода. Таким образом пользователь создавая, например, связки задач Tie явно не передает user_id, и 
    созданная запись будет обязательно связана с ним.
    
    Общий тест всей совокупности CRUD-методов:
        - создание нескольких пользователей с их данными
        - проверка правильности изначальной записи
        - тесты обновления / удаления
        - тесты недопустимых операций: запись / обновление / удаление "чужих" данных, user_id не свой
        
    1. Создаем пользователя     User
    2. Создаем все его Ties         Ties
    3. Создаем все его Tails            Tails
    4. Создаем все его Tales                Tales
"""


@dataclass
class Accounts:
    account_1: FakeUser
    account_2: FakeUser

    def __iter__(self):
        for item in self.__dict__.values():
            yield item


def fill_test_model(model, level='1') -> BaseModel:
    """Генератор для заполнения простой модели: случайные имена строковых полей"""
    _level = level
    def generate_value(name, info):
        if not info.is_required():
            return info.default

        if info.annotation == str:
            return f"{name}_{_level}"
        else:
            if get_origin(info.annotation) == list:
                target_type = get_args(info.annotation)[0]
                return [fill_test_model(target_type, f'{_level}{i + 1}') for i in range(random.randint(2, 4))]
            else:
                if issubclass(info.annotation, Enum):
                    return random.choice(list(info.annotation))
                else:
                    return fill_test_model(get_origin(info.annotation))

    data = {}
    for name, info in model.model_fields.items():
        data[name] = generate_value(name, info)
    #
    return model(**data)

@pytest.fixture(scope="module")
async def test_data():
    return Accounts(
        account_1 = fill_test_model(FakeUser, 1),
        account_2 = fill_test_model(FakeUser, 2),
    )

"""
    Изначально я думал что для каждого типа провекрки будет своя тест_функция, изменения в состоянии БД будут сохраняться,
    а полный откат будет только по завершению всех тестов модуля. Но в этом режиме были какие-то проблемы с асинхронными
    вызовами между тестами, в итоге оставил эту затею и поместил все тесты просто в одну функцию. В конфтесте настроено
    на отдельную сессию и роллбек после на каждый тест.
"""

async def test_all_crud_operations(db_session: AsyncSession, test_data):
    # создание всех пользователей и создание всех их внутренних данных
    for user in test_data:
        _user = await UserRepository.create(db_session, hashed_token=user.hashed_token)
        user.id = _user.id
        for tie in user.ties:
            _tie = await TieRepository.create(db_session, user_id=_user.id, desc=tie.desc, tie_type=tie.type)
            for tail in tie.tails:
                _tail = await TailRepository.create(db_session, user_id=_user.id, tie_id=_tie.id, desc=tail.desc)
                for tale in tail.tales:
                    _tale = await TaleRepository.create(db_session, user_id=_user.id, tail_id=_tail.id, desc=tale.desc)

    # STEP I
    # проверка правильности создания
    for user in test_data:
        _user = await UserRepository.get(db_session, hashed_token=user.hashed_token)

        # пользователь по его токену и названиям его связок
        assert user.hashed_token == _user.hashed_token
        assert [t.desc for t in user.ties] == [t.desc for t in _user.ties]

        # самих связок
        for tie, tie_id in zip(user.ties, [t.id for t in _user.ties]):
            _tie = await TieRepository.tie(db_session, user_id=_user.id, tie_id=tie_id)
            # явно выгруженная связка по названию и типу
            assert tie.desc == _tie.desc
            assert tie.type == _tie.type

            for tail, tail_id in zip(tie.tails, [t.id for t in _tie.tails]):
                _tail = await TailRepository.tail(db_session, user_id=_user.id, tail_id=tail_id)
                # явно выгруженные хвосты по названию и !--статусу--!
                assert tail.desc == _tail.desc
                # assert tail.status == _tail.status

                # изменения в Tail
                nd = f'{_tail.desc} UPDATED'
                ns = random.choice([e.value for e in TailStatus])
                await TailRepository.update(db_session, tail_id=tail_id, user_id=_user.id, desc=nd, status=ns)
                _tail = await TailRepository.tail(db_session, user_id=_user.id, tail_id=tail_id)
                assert _tail.desc == nd
                assert _tail.status.value == ns

                for tale, tale_id in zip(tail.tales, [t.id for t in _tail.tales]):
                    _tale = await TaleRepository.tale(db_session, user_id=_user.id, tale_id=tale_id)
                    # явно выгруженная история по названию
                    assert tale.desc == _tale.desc

    # STEP II
    # проверка разрешенных и запрещенных действий: измения ЧУЖИХ данных
    userX, userY = test_data.account_1.id, test_data.account_2.id

    # читаю все связки юзера - чужого нельзя по определению, на входе только user_id (но в api нельзя его вручную вбить)
    all_ties = await TieRepository.ties(db_session, user_id=userX)
    assert [tie.desc for tie in all_ties] == [tie.desc for tie in test_data.account_1.ties]

    # создание связки (чужую создать нельзя: создается по user_id же только)
    tie_for_del = await TieRepository.create(db_session, user_id=userX, desc="Tie for del", tie_type=TieType.base)
    assert type(tie_for_del) == Tie

    # попытки читать чужую связку (получаем ничего)
    none_tie = await TieRepository.tie(db_session, tie_id=tie_for_del.id, user_id=userY)
    assert none_tie is None

    # попытка создать хвост в чужой связки
    with pytest.raises(HTTPException) as exc:
        await TailRepository.create(db_session, desc="Tail for del", tie_id=tie_for_del.id, user_id=userY)
    assert exc.value.status_code == 400

    # создаем свой хвост
    tail_for_del = await TailRepository.create(db_session, desc="Tail for del", tie_id=tie_for_del.id, user_id=userX)
    assert type(tail_for_del) == Tail

    # попытка прочесть чужой хвост
    none_tail = await TailRepository.tail(db_session, tail_id=tail_for_del.id, user_id=userY)
    assert none_tail is None

    # попытка прочесть все хвосты из чужой связки
    none_tails = await TailRepository.tails(db_session, tie_id=tie_for_del.id, user_id=userY)
    assert none_tails == []

    # попытка создать историю в чужом хвосте
    with pytest.raises(HTTPException) as exc:
        await TaleRepository.create(db_session, desc="Tale for del", tail_id=tail_for_del.id, user_id=userY)
    assert exc.value.status_code == 400

    # создание своей истории
    tale_for_del = await TaleRepository.create(db_session, desc="Tale for del", tail_id=tail_for_del.id, user_id=userX)
    assert type(tale_for_del) == Tale

    # попытка получения чужой истории
    none_tale = await TaleRepository.tale(db_session, tale_id=tale_for_del.id, user_id=userY)
    assert none_tale is None

    # попытка удаления чужой истории
    with pytest.raises(HTTPException) as exc:
        await TaleRepository.delete(db_session, tale_id=tale_for_del.id, user_id=userY)
    assert exc.value.status_code == 400

    # удаление своей истории
    deleted_tale = await TaleRepository.delete(db_session, tale_id=tale_for_del.id, user_id=userX)
    assert deleted_tale.id == tale_for_del.id

    # попытка удаления чужого хвоста
    with pytest.raises(HTTPException) as exc:
        await TailRepository.delete(db_session, tail_id=tail_for_del.id, user_id=userY)
    assert exc.value.status_code == 400
    assert exc.value.detail == "У пользователя нет такого хвоста!"

    # удаление своего хвоста
    deleted_tail = await TailRepository.delete(db_session, tail_id=tail_for_del.id, user_id=userX)
    assert deleted_tail.id == tail_for_del.id

    # попытка удалить чужую связку
    with pytest.raises(HTTPException) as exc:
        await TieRepository.delete(db_session, tie_id=tie_for_del.id, user_id=userY)
    assert exc.value.status_code == 400

    # удаляем свою связку
    deleted_tie = await TieRepository.delete(db_session, tie_id=tie_for_del.id, user_id=userX)
    assert deleted_tie.id == tie_for_del.id
