from collections import namedtuple

from .SQLite import Sqlite3_Database
from .Enum_classes import Flags


class User:
    def __init__(self, id, **kwargs):
        self.id: int = id
        if len(kwargs):
            self.username: str = kwargs["username"]
            self.status: bool = kwargs["status"]
            self.referral_link: str = kwargs["referral_link"]
            self.referral_boss_id: int = kwargs["referral_boss_id"]
            self.withdrawal_account: str = kwargs["withdrawal_account"]
            self.balance: float = kwargs["balance"]
            self.bonus_account: float = kwargs["bonus_account"]
            self.earnings_from_contracts: float = kwargs["earnings_from_contracts"]
            self.earnings_from_partners: float = kwargs["earnings_from_partners"]
            self.flag: Flags = Flags(kwargs["flag"])
            self.bot_message_id: int = kwargs["bot_message_id"]
            self.delete_message_id: int = kwargs["delete_message_id"]

        else:
            self.username: str = ""
            self.status: bool = True
            self.referral_link: str = ""
            self.referral_boss_id: int = 0
            self.withdrawal_account: str = ""
            self.balance: float = 0.0
            self.bonus_account: float = 0.0
            self.earnings_from_contracts: float = 0.0
            self.earnings_from_partners: float = 0.0
            self.flag: Flags = Flags.NONE
            self.bot_message_id: int = 0
            self.delete_message_id: int = 0

    def __iter__(self):
        dict_class = self.__dict__
        Result = namedtuple("Result", ["name", "value"])
        for attr in dict_class:
            if not attr.startswith("__"):
                if attr != "flag":
                    yield Result(attr, dict_class[attr])
                else:
                    yield Result(attr, dict_class[attr].value)


class Users(Sqlite3_Database):
    def __init__(self, db_file_name, table_name, *args) -> None:
        Sqlite3_Database.__init__(self, db_file_name, table_name, *args)
        self.len = len(self.get_keys())

    def add(self, obj: User) -> None:
        self.add_row(obj)
        self.len += 1

    def __len__(self):
        return self.len

    def __delitem__(self, key):
        self.del_instance(key)
        self.len -= 1

    def __iter__(self) -> User:
        keys = self.get_keys()
        for id in keys:
            user = self.get(id)
            yield user
    def get(self, id: int) -> User | bool:
        if id in self:
            obj_tuple = self.get_elem_sqllite3(id)
            obj = User(id=obj_tuple[0],
                       username=obj_tuple[1],
                       status=obj_tuple[2],
                       referral_link=obj_tuple[3],
                       referral_boss_id=obj_tuple[4],
                       withdrawal_account=obj_tuple[5],
                       balance=obj_tuple[6],
                       bonus_account=obj_tuple[7],
                       earnings_from_contracts=obj_tuple[8],
                       earnings_from_partners=obj_tuple[9],
                       flag=Flags(obj_tuple[10]),
                       bot_message_id=obj_tuple[11],
                       delete_message_id=obj_tuple[12])
            return obj
        return False

    def get_referral_boss(self, id: int) -> str | None:
        answer = self.get_by_other_field(field="id", value=id, username="username")
        answer = [el[0] for el in answer]
        return answer[0]

    def get_ref_1_lvl(self, id: int) -> tuple:
        answer = self.get_by_other_field(field="referral_boss_id", value=id, username="username", id="id")
        username = [el[0] for el in answer]
        keys = [el[1] for el in answer]
        return username, keys

    def get_ref_2_lvl(self, id: int):
        ref_1_lvl = self.get_ref_1_lvl(id)[1]

        ref_2_lvl_username = []
        ref_2_lvl_keys = []
        for id in ref_1_lvl:
            ref_2_lvl_username.append(self.get_ref_1_lvl(id)[0])
            ref_2_lvl_keys.append(self.get_ref_1_lvl(id)[1])

        usernames = []
        keys = []
        for el in range(len(ref_2_lvl_username)):
            for i in ref_2_lvl_username[el]:
                usernames.append(i)

        for el in range(len(ref_2_lvl_keys)):
            for i in ref_2_lvl_keys[el]:
                keys.append(i)

        return usernames, keys

    def get_ref_3_lvl(self, id: int):
        ref_2_lvl = self.get_ref_2_lvl(id)[1]
        ref_3_lvl_username = []

        for id in ref_2_lvl:
            ref_3_lvl_username.append(self.get_ref_1_lvl(id)[0])
        result = []
        for el in range(len(ref_3_lvl_username)):
            for i in ref_3_lvl_username[el]:
                result.append(i)
        return result
