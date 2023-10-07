from rest_framework import serializers
from employees.models import Employee


class EmployeeSerializers(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = ('first_name', 'last_name', 'patronymic', 'email')

    def create(self, validated_data):
        """
        :param validated_data: Данные, переданные при создании нового пользователя
        Метод переопределен для корректного создания нового пользователя.
        Пароль указанный при создании пользователя хэшируется, появляется возможность авторизации по JWT.
        :return: Создается новый экземпляр класса CustomUser
        """

        new_employee = Employee.objects.create_user(**validated_data)
        return new_employee


class EmployeeListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'
