from bookkeeper.repository.sqlite_repository import SqliteRepository
from bookkeeper.models.expense import Expense
from datetime import datetime
import sqlite3

import pytest
from dataclasses import dataclass, field


@pytest.fixture
def custom_class():
    class Custom():
        amount = 0
        category = 0
        expense_date = datetime.now().strftime("%d/%m/%Y, %H:%M")
        added_date = datetime.now().strftime("%d/%m/%Y, %H:%M")
        comment = ''
        pk = 0

        def __eq__(self, other):
            return other.pk == self.pk and other.amount == self.amount
    return Custom

@pytest.fixture
def repo():
    return SqliteRepository(db_file='./tests/test_repository/test.db', cls=Expense) #idk maybe shuold be more abstract

def test_crud(repo, custom_class):
    obj = custom_class()

    pk = repo.add(obj)
    assert obj.pk == pk
    assert repo.get(pk) == obj
    obj2 = custom_class()
    obj2.pk = pk
    repo.update(obj2)
    assert repo.get(pk) == obj2
    repo.delete(pk)
    assert repo.get(pk) is None


def test_cannot_add_with_pk(repo, custom_class):
    obj = custom_class()
    obj.pk = 1
    with pytest.raises(ValueError):
        repo.add(obj)


def test_cannot_add_without_pk(repo):
    with pytest.raises(ValueError):
        repo.add(0)


def test_cannot_delete_unexistent(repo):
    with pytest.raises(KeyError):
        repo.delete(1000)


def test_cannot_update_without_pk(repo, custom_class):
    obj = custom_class()
    with pytest.raises(ValueError):
        repo.update(obj)


def test_get_all(repo, custom_class):
    conn = sqlite3.connect(repo.db_file)
    c = conn.cursor()
    c.execute(f"DELETE FROM {repo.table_name}")
    conn.commit()
    conn.close()
    objects = [custom_class() for i in range(5)]

    for o in objects:
        repo.add(o)
    assert repo.get_all() == objects


def test_get_all_with_condition(repo, custom_class):
    objects = []
    for i in range(5):
        o = custom_class()
        o.category = 5
        repo.add(o)
        objects.append(o)
    assert repo.get_all({'category': 5}) == objects



