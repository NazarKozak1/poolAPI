from django.contrib import admin
from django.http import HttpResponse
from django.urls import path

def test_view(request):
    return HttpResponse("Django is working!")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("test/", test_view),
]
