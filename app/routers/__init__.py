from .users import router as users_router
from .token import router as token_router
from .todos import router as todos_router

routers = [
    users_router,
    token_router,
    todos_router
]
