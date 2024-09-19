# fastapi_app.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# FastAPI routers
from poolAPI.router.test import router as test_router
from poolAPI.router.lightning_settings import router as light_settings_router
from poolAPI.router.backwash_settings import router as backwash_settings_router
from poolAPI.router.ph_settings import router as ph_settings_router

def create_fastapi_app() -> FastAPI:
    app = FastAPI(title="FastAPI Sub-app", debug=True)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add routes
    app.include_router(test_router)
    app.include_router(light_settings_router)
    app.include_router(backwash_settings_router)
    app.include_router(ph_settings_router)

    return app