from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from rest_framework import generics, status, serializers
from rest_framework.response import Response
from suppliers.models import Vendors, Factory, RetailChains
from suppliers.serializers import VendorSerializer
from django.core.exceptions import ObjectDoesNotExist


class VendorCreateAPIView(generics.CreateAPIView):
    serializer_class = VendorSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        # Извлекаем данные из запроса
        title = request.data.get('title')
        supplier_content_type_choice = request.data.get('supplier_content_type')
        supplier_id = request.data.get('supplier_id')

        if supplier_content_type_choice and supplier_id:
            if supplier_content_type_choice == 9:
                try:
                    if Factory.objects.get():

                        # Пытаемся получить ContentType для модели поставщика
                        supplier_content_type = ContentType.objects.get_for_id(supplier_content_type_choice)
                        related_supplier = Factory.objects.get(id=supplier_id)
                        # Создаем объект Vendors
                        try:
                            vendor = Vendors.objects.create(
                                title=title,
                                supplier_content_type=supplier_content_type,
                                supplier_id=supplier_id,
                                supplier_title=related_supplier.title
                            )

                            serializer = self.get_serializer(vendor)
                            return Response(serializer.data, status=status.HTTP_201_CREATED)

                        except IntegrityError:
                            return Response({'detail': 'ИП с таким названием уже существует.'},  #: Работает
                                            status=status.HTTP_400_BAD_REQUEST)

                except ObjectDoesNotExist:    #: Работает
                    return Response({'detail': f'Поставщик c ID: {supplier_id} не зарегистрирован'}, status=status.HTTP_400_BAD_REQUEST)

            else:  #: Работает
                return Response({'detail': 'Указанный некорректный id типа поставщика. '
                                           'Укажите: supplier_content_type:9 (Завод), '
                                           'supplier_content_type:11 (Розничная сеть)'},
                                status=status.HTTP_400_BAD_REQUEST)

        if supplier_content_type_choice or supplier_id:  #: Работает
            return Response({'detail': 'Для создания связи с поставщиком необходимо указать '
                                       'supplier_content_type: 9 (Завод) или 11 (Розничная сеть) '
                                       'и supplier_id (id поставщика)'},
                            status=status.HTTP_400_BAD_REQUEST)

        else:
            try:
                Vendors.objects.create(title=title)

            except IntegrityError:  #: Работает
                return Response({'detail': 'ИП с таким названием уже существует.'}, status=status.HTTP_400_BAD_REQUEST)

            serializer.is_valid()  #: Работает
            return Response(serializer.data, status=status.HTTP_201_CREATED)


