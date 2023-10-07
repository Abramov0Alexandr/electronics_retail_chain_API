from django.contrib import admin
from .models import Contacts


@admin.register(Contacts)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'country', 'city', 'street', 'building_number')
    list_display_links = ('email', )
    list_filter = ('country', )
