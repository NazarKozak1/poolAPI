import os
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

