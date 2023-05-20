from .Users import User, Users
from .Contracts import Contract, Contracts
from .Promocodes import Promocode, Promocodes
from .UserPromocodes import UserPromocode, UserPromocodes
from .Enum_classes import Flags

db_file_name = "bot/db/database"
users = Users(db_file_name=db_file_name, table_name="users")
contracts = Contracts(db_file_name=db_file_name, table_name="contracts")
promocodes = Promocodes(db_file_name=db_file_name, table_name="promocode")
userPromocodes = UserPromocodes(db_file_name, table_name="user_promocode")
__all__ = ("User", "Users", "Contract", "Contracts", "Promocode", "Promocodes", "Flags", "users", "contracts",
           "promocodes", "userPromocodes", "UserPromocode", "UserPromocodes")
