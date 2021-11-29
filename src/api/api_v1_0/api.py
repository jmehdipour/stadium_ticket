from fastapi import APIRouter, Depends

from src.api.api_v1_0.endpoints.stadiums import router as stadium_router
from src.api.api_v1_0.endpoints.matches import router as match_router
from src.api.middlewares import is_admin

router = APIRouter()

router.include_router(stadium_router, tags=['stadiums'])
router.include_router(match_router, tags=['matches'])
