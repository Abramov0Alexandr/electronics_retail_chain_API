from django.contrib import admin

from suppliers.models import Vendors
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
    list_display = ('id', 'title', 'registration_date', 'contacts',
                    'supplier_id', 'supplier_content_type', 'supplier_title', 'debt_amount')
    date_hierarchy = 'registration_date'
    list_display_links = ('title', )
    empty_value_display = "Отсутствует"


@admin.register(Vendors)
class UserAdmin(admin.ModelAdmin):
    list_display_links = ('title', )
    list_display = ('id', 'title', 'registration_date', 'contacts',
                    'supplier_id', 'supplier_content_type', 'supplier_title', 'debt_amount')
    empty_value_display = "Зарегистрирован как поставщик"

