from django.contrib import admin
from django.urls import path, include
from .views import index, folder
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', index),
    path('bulk_detection', folder)
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)