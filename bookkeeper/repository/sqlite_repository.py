"""
Модуль описывает репозиторий, работающий в СУБД sqlite
"""

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
        if getattr(obj, 'pk', None) != 0:
            raise ValueError(f'trying to add object {obj} with filled `pk` attribute')
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

        return adapter(res[-1]) if res else None

    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:

        with sqlite3.connect(self.db_file) as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            if where is None:
                cur.execute(f'SELECT * FROM {self.table_name}')
                res = cur.fetchall()
            else:
                columns, values = list(where.keys()), \
                                  list(where.values())
                cur.execute(f'SELECT * FROM {self.table_name} WHERE {columns[0]}=(?)',
                            [values[0]])
                res = cur.fetchall()
                if columns[1:]:
                    res = [x_res for x_res in res if all(x_res[column] == value for column,
                                                                                    value in zip(columns[1:],
                                                                                                 values[1:]))]
            adapter = adapters[self.table_name]
            res = list(map(adapter, res))
        con.close()
        return res

    def update(self, obj: T) -> None:

        if obj.pk == 0:
            raise ValueError('attempt to update object with unknown primary key')

        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            names = list(self.fields.keys())
            values = [getattr(obj, x) for x in self.fields]
            update_command = f'UPDATE {self.table_name} SET ' + ', '.join(
                [f'{name} = ?' for name in names]) + ' WHERE pk = ?'
            cur.execute(update_command, values + [obj.pk])
        con.close()

    def delete(self, pk: int) -> None:
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(f'DELETE FROM {self.table_name} WHERE pk=  ?', [pk])
            if cur.rowcount == 0:
                raise KeyError('Object with such pk do not exist in the database')
        con.close()
