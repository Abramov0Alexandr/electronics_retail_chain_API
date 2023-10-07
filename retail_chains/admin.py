from django.contrib import admin
from .models import RetailNetwork


@admin.register(RetailNetwork)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'debt_amount', 'registration_date')
    list_display_links = ('title', )
