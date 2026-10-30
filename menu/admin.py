from django.contrib import admin
from .models import Menu, MenuComment, MenuReaction

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'image')
    search_fields = ('name',)
    ordering = ('name',)
    list_per_page = 25


@admin.register(MenuComment)
class MenuCommentAdmin(admin.ModelAdmin):
    list_display = ("menu", "name", "created_at")
    list_filter = ("created_at",)
    search_fields = ("menu__name", "name", "body")
    readonly_fields = ("created_at",)
    list_per_page = 25


@admin.register(MenuReaction)
class MenuReactionAdmin(admin.ModelAdmin):
    list_display = ("menu", "reaction")
    list_filter = ("reaction",)
    search_fields = ("menu__name",)
    list_per_page = 25


