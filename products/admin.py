from django.contrib import admin
from .models import Products


@admin.register(Products)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'model', 'release_date', 'manufacturer')
    list_display_links = ('title', )
    date_hierarchy = 'release_date'
    empty_value_display = "Не указано"
