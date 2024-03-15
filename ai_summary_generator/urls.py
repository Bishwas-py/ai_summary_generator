from django.contrib import admin
from django.urls import path, include
from djapy import openapi

urlpatterns = [
    path('', openapi.urls),
    path('admin/', admin.site.urls),
    path('article/', include('article.urls')),
]
