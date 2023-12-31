"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from app.api import api
from django.contrib import admin
from django.http.response import HttpResponseRedirect
from django.urls import path
from django.views.static import serve

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", lambda request: HttpResponseRedirect("/index.html")),
    path("api/", api.urls),
    path("<path:path>", serve, {"document_root": "backend/frontend_dist"}, name="root"),
]
