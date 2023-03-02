"""
Модуль описывает репозиторий, работающий в СУБД sqlite
"""

from itertools import count
from typing import Any
from inspect import get_annotations
from bookkeeper.utils import adapters
import sqlite3

from bookkeeper.repository.abstract_repository import AbstractRepository, T

class SqliteRepository(AbstractRepository[T]):
    """
    Репозиторий, работающий в sqlite. Хранит данные в базе данных.
    """

    def __init__(self, db_file: str, cls: type) -> None:

        self.db_file = db_file
        self.table_name = cls.__name__.lower()
        self.fields = get_annotations(cls, eval_str=True)
        self.fields.pop('pk')

    def add(self, obj: T) -> int:

        names = ', '.join(self.fields.keys())
        p = ', '.join("?" * len(self.fields))
        values = [getattr(obj, x) for x in self.fields]
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(
                f'INSERT INTO {self.table_name} ({names}) VALUES ({p})', values
            )
            obj.pk = cur.lastrowid
        con.close()
        return obj.pk

    def get(self, pk: int) -> T | None:
        with sqlite3.connect(self.db_file) as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(
                f'SELECT * FROM {self.table_name} WHERE pk=(?)', [pk]
            )
            res = cur.fetchall()
        con.close()
        adapter = adapters[self.table_name]

        return adapter(res[-1])  if res else None

    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        pass

    def update(self, obj: T) -> None:
        pass

    def delete(self, pk: int) -> None:
        pass





        

