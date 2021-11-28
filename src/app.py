from fastapi import FastAPI

from src.api.api_v1_0.api import router as api_router_v1_0
from src.api.general.api import router as api_router_general
from src.config import get_settings

app = FastAPI(title=get_settings().APP_NAME)

app.include_router(api_router_v1_0, prefix='/api_v1.0')
app.include_router(api_router_general, prefix='/general')

if get_settings().DEBUG:
    if __name__ == "__main__":
        import uvicorn

        uvicorn.run(app, host="127.0.0.1", port=8000, debug=True)
