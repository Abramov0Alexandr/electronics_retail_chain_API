from django.contrib import admin
from employees.models import Employee


@admin.register(Employee)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name', 'employer',)
    list_display_links = ('email', )
    list_filter = ('employer', )
