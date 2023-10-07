from django.contrib import admin
from .models import Factory


@admin.register(Factory)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'registration_date',)
    list_display_links = ('title', )
