from django.contrib import admin
from .models import Menu

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'image')
    search_fields = ('name',)
    ordering = ('name',)
    list_per_page = 25


