from django.contrib import admin
from suppliers.models.factories import Factory


@admin.register(Factory)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'registration_date', 'contacts',)
    list_display_links = ('title',)


# @admin.register(RetailChains)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('id', 'title', 'debt_amount', 'registration_date')
#     list_display_links = ('title', )
#
# @admin.register(Vendors)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('id', 'title', 'debt_amount', 'registration_date')
#     list_display_links = ('title', )
