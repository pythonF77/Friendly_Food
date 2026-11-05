from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from my_admin.views import setup_admin

urlpatterns = [
    path('setup-admin/', setup_admin, name='setup_admin'),
    path('admin/', admin.site.urls),
    path('', include('menu.urls')),
]
# if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




