from .user import user_routers
from .manager import manager_routers

routers = (*user_routers, *manager_routers)
