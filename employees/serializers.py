from rest_framework import serializers
from employees.models import Employee


class EmployeeCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания нового объекта модели Employee.
    """

    class Meta:
        model = Employee
        fields = ('id', 'first_name', 'last_name', 'patronymic', 'email', 'password')

    def create(self, validated_data):
        """
        :param validated_data: Данные, переданные при создании нового работника
        Метод переопределен для корректного создания нового работника и хеширования значения поля password.
        :return: Экземпляр класса Employee
        """

        new_employee = Employee.objects.create_user(**validated_data)

        return new_employee


class EmployeeListSerializer(serializers.ModelSerializer):
    """
    Сериализатор для вывода списка объектов модели Employee.
    """

    class Meta:
        model = Employee
        fields = ('id', 'first_name', 'last_name', 'patronymic', 'email', 'date_joined')


class AdminEmployeeListSerializer(serializers.ModelSerializer):
    """
    Сериализатор для вывода списка объектов модели Employee с полной информацией о сотрудниках.
    """

    class Meta:
        model = Employee
        fields = '__all__'
