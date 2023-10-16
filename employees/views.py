from rest_framework import generics
from rest_framework.permissions import AllowAny
from employees.models import Employee
from .serializers import EmployeeCreateSerializer, EmployeeListSerializer, AdminEmployeeListSerializer


class CreateEmployeeApiView(generics.CreateAPIView):
    """
    Контроллер для создания нового объекта модели Employee.
    """

    serializer_class = EmployeeCreateSerializer
    permission_classes = [AllowAny]


class EmployeesListAPIView(generics.ListAPIView):
    """
    Контроллер для получения списка объектов модели Employee.
    В случае, если список запрашивает суперпользователь, то выводится полная информация о сотрудниках.
    В случае, если список получает обычный сотрудник, то выводится только основная информация.
    """

    queryset = Employee.objects.all()

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return AdminEmployeeListSerializer

        return EmployeeListSerializer


class DeleteEmployeeApiView(generics.DestroyAPIView):
    """
    Контроллер для удаления объекта модели Employee.
    Контроллер позволяет удалить только самого себя.
    Суперпользователь может удалить любого пользователя.
    """

    def get_queryset(self):

        if self.request.user.is_superuser:
            return Employee.objects.all()

        return Employee.objects.filter(email=self.request.user.email)
