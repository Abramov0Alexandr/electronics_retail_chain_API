from django.contrib import admin
from .models import Products


@admin.register(Products)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'model', 'release_date', )
    list_display_links = ('title', )
