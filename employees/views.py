from rest_framework import generics

from employees.models import Employee
from employees.serializers import EmployeeSerializers, EmployeeListSerializers


class CreateEmployeeApiView(generics.CreateAPIView):
    serializer_class = EmployeeSerializers


class EmployeesListAPIView(generics.ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeListSerializers


class DeleteEmployeeApiView(generics.DestroyAPIView):
    queryset = Employee.objects.all()
