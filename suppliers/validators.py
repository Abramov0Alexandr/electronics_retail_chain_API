from rest_framework import status
from rest_framework.validators import ValidationError
from suppliers.models import Factory, RetailChains, Vendors


class RequiredSupplierField:

    def __call__(self, value):
        supplier_content_type = value.get('supplier_content_type')
        supplier_id = value.get('supplier_id')

        if (supplier_content_type and not supplier_id) or (supplier_id and not supplier_content_type):

            raise ValidationError(
                {
                    'message':
                        {'supplier_content_type': 'Для создания связи с поставщиком необходимо указать '
                                                  '9 (для связи с заводом) '
                                                  '10 (для связи с индивидуальным предпринимателем) '
                                                  '11 (для розничной сети)',
                         'supplier_id': 'id поставщика',
                         'status': status.HTTP_400_BAD_REQUEST
                         }
                }
            )


class NewTitleValidationError:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        new_title = value.get(self.field)

        if Factory.objects.filter(title=new_title).exists():
            raise ValidationError(
                {
                    "title": [f"Название \'{new_title}\' уже используется."],
                    'status': status.HTTP_400_BAD_REQUEST
                }
            )

        if RetailChains.objects.filter(title=new_title).exists():
            raise ValidationError(
                {
                    "title": [f"Название \'{new_title}\' уже используется."],
                    'status': status.HTTP_400_BAD_REQUEST
                }
            )

        if Vendors.objects.filter(title=new_title).exists():
            raise ValidationError(
                {
                    "title": [f"Название \'{new_title}\' уже используется."],
                    'status': status.HTTP_400_BAD_REQUEST
                }
            )
