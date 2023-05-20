from collections import namedtuple

from .SQLite import Sqlite3_Database


class UserPromocode:
    def __init__(self, id, **kwargs):
        self.id: int = id
        if len(kwargs):
            self.name: int = kwargs["name"]
            self.user_id: int = kwargs["user_id"]

        else:
            self.user_id: int = 0
            self.name: str = ""

    def __iter__(self):
        dict_class = self.__dict__
        Result = namedtuple("Result", ["name", "value"])
        for attr in dict_class:
            if not attr.startswith("__"):
                if attr != "flag":
                    yield Result(attr, dict_class[attr])
                else:
                    yield Result(attr, dict_class[attr].value)


class UserPromocodes(Sqlite3_Database):
    def __init__(self, db_file_name, table_name, *args) -> None:
        Sqlite3_Database.__init__(self, db_file_name, table_name, *args)
        self.len = len(self.get_keys())

    def add(self, obj: UserPromocode) -> None:
        self.add_row(obj)
        self.len += 1

    def __len__(self):
        return self.len

    def __delitem__(self, id):
        self.del_instance(id)
        self.len -= 1

    def all_user_contracts(self, id) -> list:
        result = self.get_by_other_field(value=id, field="user_id", attr="*")
        return result

    def get_by_name(self, name) -> UserPromocode | bool:
        obj_tuple = self.get_by_other_field(value=name, field="name", attr="*")

        if obj_tuple:
            obj_tuple = obj_tuple[0]
            obj = UserPromocode(id=obj_tuple[0],
                                name=obj_tuple[1],
                                user_id=obj_tuple[2],
                                )
            return obj
        return False

    def get(self, id: int) -> UserPromocode | bool:
        if id in self:
            obj_tuple = self.get_elem_sqllite3(id)
            obj = UserPromocode(id=obj_tuple[0],
                            name=obj_tuple[1],
                            user_id=obj_tuple[2],
                            )

            return obj
        return False
