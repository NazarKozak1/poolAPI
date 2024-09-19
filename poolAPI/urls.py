from django.urls import path, re_path
from django.contrib import admin
from django.http import HttpResponse
from fastapi.middleware.wsgi import WSGIMiddleware
from .fastapi_app import create_fastapi_app

fastapi_app = create_fastapi_app()

def index(request):
    return HttpResponse("Django is working")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    #re_path(r'^api/.*', WSGIMiddleware(fastapi_app)),  # FastAPI under '/api/' route
]