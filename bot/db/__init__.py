from .Users import User, Users
from .Contracts import Contract, Contracts
from .Enum_classes import Flags

db_file_name = "bot/db/database"
users = Users(db_file_name=db_file_name, table_name="users")
contracts = Contracts(db_file_name=db_file_name, table_name="contracts")

__all__ = ("User", "Users", "Contract", "Contracts", "Flags", "users", "contracts")
