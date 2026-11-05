from django.contrib import admin
from django.urls import path, include
from django.urls import re_path
from my_admin.views import serve_uploaded_image, setup_admin

urlpatterns = [
    path('setup-admin/', setup_admin, name='setup_admin'),
    path('admin/', admin.site.urls),
    path('', include('menu.urls')),
    re_path(r'^media/(?P<path>.*)$', serve_uploaded_image, name='uploaded_image'),
]



