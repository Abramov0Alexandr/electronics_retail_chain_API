from django.contrib import admin
from suppliers.models.factories import Factory
from suppliers.models.retail_chains import RetailChains


@admin.register(Factory)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'registration_date', 'contacts',)
    date_hierarchy = 'registration_date'
    list_display_links = ('title',)
    empty_value_display = "Не указано"


@admin.register(RetailChains)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'debt_amount', 'supplier', 'registration_date', 'contacts', 'registration_date')
    date_hierarchy = 'registration_date'
    list_display_links = ('title', )
    empty_value_display = "Отсутствует"

#
# @admin.register(Vendors)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('id', 'title', 'debt_amount', 'registration_date')
#     list_display_links = ('title', )
