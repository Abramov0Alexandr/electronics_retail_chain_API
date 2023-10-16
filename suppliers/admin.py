from django.contrib import admin
from django.db.models import QuerySet
from suppliers.models import Vendors
from suppliers.models.factories import Factory
from suppliers.models.retail_chains import RetailChains


@admin.register(Factory)
class FactoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'registration_date', 'contacts',)
    date_hierarchy = 'registration_date'
    list_display_links = ('title',)
    empty_value_display = "Отсутствует"


@admin.register(RetailChains)
class RetailChainsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'registration_date', 'contacts',
                    'supplier_id', 'supplier_content_type', 'supplier_title', 'debt_amount')
    date_hierarchy = 'registration_date'
    list_display_links = ('title', )
    empty_value_display = "Отсутствует"
    readonly_fields = ('supplier_title',)
    actions = ('cancel_debt',)

    @admin.action(description='Сбросить задолженность')
    def cancel_debt(self, request, queryset: QuerySet):
        queryset.update(debt_amount=0.00)


@admin.register(Vendors)
class VendorsAdmin(admin.ModelAdmin):
    list_display_links = ('title', )
    list_display = ('id', 'title', 'registration_date', 'contacts',
                    'supplier_id', 'supplier_content_type', 'supplier_title', 'debt_amount')
    empty_value_display = "Зарегистрирован как поставщик"
    readonly_fields = ('supplier_title',)
    actions = ('cancel_debt',)

    @admin.action(description='Сбросить задолженность')
    def cancel_debt(self, request, queryset: QuerySet):
        queryset.update(debt_amount=0.00)
