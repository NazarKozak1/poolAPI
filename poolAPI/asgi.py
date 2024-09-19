"""import os
from django.apps import apps
from django.conf import settings
from django.core.wsgi import get_wsgi_application
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.wsgi import WSGIMiddleware


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "poolAPI.settings")

apps.populate(settings.INSTALLED_APPS)

# FastAPI routers
from poolAPI.router.test import router as test_router
from poolAPI.router.lightning_settings import router as light_settings_router
from poolAPI.router.backwash_settings import router as backwash_settings_router
from poolAPI.router.ph_settings import router as ph_settings_router


# Django's WSGI-app
django_application = get_wsgi_application()
a = 3
def get_application() -> FastAPI:
    # FastAPI
    app = FastAPI(title="My Project", openapi_url=f"{settings.API_V1_STR}/openapi.json", debug=True)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Django route "/django"
    app.mount(f"{settings.WSGI_APP_URL}", WSGIMiddleware(django_application))

    return app

app = get_application()

# adding routes
app.include_router(test_router, prefix=settings.API_V1_STR)
app.include_router(light_settings_router, prefix=settings.API_V1_STR)
app.include_router(backwash_settings_router, prefix=settings.API_V1_STR)
app.include_router(ph_settings_router, prefix=settings.API_V1_STR)
"""

import os
from django.core.asgi import get_asgi_application
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "poolAPI.settings")


django_asgi_app = get_asgi_application()


fastapi_app = FastAPI(
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# Add CORS middleware to FastAPI
fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

fastapi_app.mount("/static", StaticFiles(directory=settings.STATIC_ROOT), name="static")

# FastAPI routers
from poolAPI.router.test import router as test_router
from poolAPI.router.lightning_settings import router as light_settings_router
from poolAPI.router.backwash_settings import router as backwash_settings_router
from poolAPI.router.ph_settings import router as ph_settings_router
from poolAPI.router.rx_settings import router as rx_settings_router
from poolAPI.router.solar_temperature_settings import router as solar_settings_router
from poolAPI.router.deck_settings import router as deck_settings_router
from poolAPI.router.schedule_1_filter_settings import router as schedule_1_filter_settings_router
from poolAPI.router.schedule_2_filter_settings import router as schedule_2_filter_settings_router
from poolAPI.router.schedule_3_filter_settings import router as schedule_3_filter_settings_router
from poolAPI.router.heating_settings import router as heating_settings_router
from poolAPI.router.status import router as status_router
from poolAPI.router.real_time_measurement import router as real_time_measurement_router
from poolAPI.router.aux_1_settings import router as aux_1_settings_router
from poolAPI.router.aux_2_settings import router as aux_2_settings_router
from poolAPI.router.aux_3_settings import router as aux_3_settings_router
from poolAPI.router.aux_4_settings import router as aux_4_settings_router
from poolAPI.router.general_settings import router as general_settings_router


fastapi_app.include_router(test_router, prefix="/api")
fastapi_app.include_router(light_settings_router, prefix="/api")
fastapi_app.include_router(backwash_settings_router, prefix="/api")
fastapi_app.include_router(ph_settings_router, prefix="/api")
fastapi_app.include_router(rx_settings_router, prefix="/api")
fastapi_app.include_router(solar_settings_router, prefix="/api")
fastapi_app.include_router(deck_settings_router, prefix="/api")
fastapi_app.include_router(schedule_1_filter_settings_router, prefix="/api")
fastapi_app.include_router(schedule_2_filter_settings_router, prefix="/api")
fastapi_app.include_router(schedule_3_filter_settings_router, prefix="/api")
fastapi_app.include_router(heating_settings_router, prefix="/api")
fastapi_app.include_router(status_router, prefix="/api")
fastapi_app.include_router(real_time_measurement_router, prefix="/api")
fastapi_app.include_router(aux_1_settings_router, prefix="/api")
fastapi_app.include_router(aux_2_settings_router, prefix="/api")
fastapi_app.include_router(aux_3_settings_router, prefix="/api")
fastapi_app.include_router(aux_4_settings_router, prefix="/api")
fastapi_app.include_router(general_settings_router, prefix="/api")


class ASGIApp:
    def __init__(self):
        self.fastapi_app = fastapi_app
        self.django_app = django_asgi_app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http" and scope["path"].startswith("/api"):
            await self.fastapi_app(scope, receive, send)
        else:
            await self.django_app(scope, receive, send)

application = ASGIApp()