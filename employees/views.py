from rest_framework import generics
from employees.models import Employee
from .serializers import EmployeeSerializer, EmployeeListSerializer


class CreateEmployeeApiView(generics.CreateAPIView):
    serializer_class = EmployeeSerializer


class EmployeesListAPIView(generics.ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeListSerializer


class DeleteEmployeeApiView(generics.DestroyAPIView):
    queryset = Employee.objects.all()
