from django.contrib import admin
from .models import Contacts


@admin.register(Contacts)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'contact_owner', 'type_owner_organization', 'email',
                    'country', 'city', 'street', 'building_number')

    list_display_links = ('contact_owner', )
    list_filter = ('country', 'type_owner_organization')
    readonly_fields = ('contact_owner', 'type_owner_organization')
    search_fields = ('contact_owner',)
    empty_value_display = "Не указано"
