from rest_framework import generics
from employees.models import Employee
from .serializers import EmployeeCreateSerializer, EmployeeListSerializer


class CreateEmployeeApiView(generics.CreateAPIView):
    """
    Контроллер для создания нового объекта модели Employee.
    """

    serializer_class = EmployeeCreateSerializer


class EmployeesListAPIView(generics.ListAPIView):
    """
    Контроллер для получения списка объектов модели Employee.
    """

    queryset = Employee.objects.all()
    serializer_class = EmployeeListSerializer


class DeleteEmployeeApiView(generics.DestroyAPIView):
    """
    Контроллер для удаления объекта модели Employee.
    """

    queryset = Employee.objects.all()
