from django.urls import path
from .apps import EmployeesConfig
from .views import CreateEmployeeApiView, EmployeesListAPIView, DeleteEmployeeApiView


app_name = EmployeesConfig.name

urlpatterns = [
    path('create/', CreateEmployeeApiView.as_view(), name='create_employee'),
    path('list/', EmployeesListAPIView.as_view(), name='employee_list'),
    path('delete/<int:pk>/', DeleteEmployeeApiView.as_view(), name='delete_employee'),
]
