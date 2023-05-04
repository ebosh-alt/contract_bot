import datetime
from collections import namedtuple

from .SQLite import Sqlite3_Database
from .Enum_classes import Flags


class Contract:
    def __init__(self, id, **kwargs):
        self.id: int = id
        if len(kwargs):
            self.count_day: int = kwargs["count_day"]
            self.amount: int = kwargs["amount"]
            self.user_id: int = kwargs["user_id"]



        else:
            self.count_day: int = 0
            self.amount: int = 0
            self.user_id: int = 0

    def __iter__(self):
        dict_class = self.__dict__
        Result = namedtuple("Result", ["name", "value"])
        for attr in dict_class:
            if not attr.startswith("__"):
                if attr != "flag":
                    yield Result(attr, dict_class[attr])
                else:
                    yield Result(attr, dict_class[attr].value)


class Contracts(Sqlite3_Database):
    def __init__(self, db_file_name, table_name, *args) -> None:
        Sqlite3_Database.__init__(self, db_file_name, table_name, *args)
        self.len = self.get_keys()

    def add(self, obj: Contract) -> None:
        self.add_row(obj)
        self.len += 1

    def __len__(self):
        return self.len

    def __delitem__(self, id):
        self.del_instance(id)
        self.len -= 1

    def all_user_contracts(self, id) -> list:
        result = self.get_by_other_field(value=id, field="user_id", amount="amount")
        return result

    def get(self, id: int) -> Contract | bool:
        if id in self:
            obj_tuple = self.get_elem_sqllite3(id)
            obj = Contract(id=obj_tuple[0],
                           count_day=obj_tuple[1],
                           amount=obj_tuple[2],
                           user_id=obj_tuple[3])

            return obj
        return False
