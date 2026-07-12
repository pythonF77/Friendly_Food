from django.urls import path
from . import views

urlpatterns= [
    path('',views.Home, name='menu_home'),
    path('menu/<int:pk>/', views.Menu_detail, name='menu_detail'),

    ]