from .users import router as users_router
from .token import router as token_router
from .items import router as items_router

routers = [
    users_router,
    token_router,
    items_router
]
