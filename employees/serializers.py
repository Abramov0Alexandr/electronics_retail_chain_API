from rest_framework import serializers
from employees.models import Employee


class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = ('first_name', 'last_name', 'patronymic', 'email', 'password')

    def create(self, validated_data):
        """
        :param validated_data: Данные, переданные при создании нового работника
        Метод переопределен для корректного создания нового работника и хеширования значения поля password.
        :return: Экземпляр класса Employee
        """

        new_employee = Employee.objects.create_user(**validated_data)

        return new_employee


class EmployeeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'
