from rest_framework import status
from rest_framework.validators import ValidationError


class RequiredSupplierField:

    def __call__(self, value):
        supplier_content_type = value.get('supplier_content_type')
        supplier_id = value.get('supplier_id')

        if supplier_content_type and not supplier_id:
            raise ValidationError(
                {
                    'message': 'Для создания связи с поставщиком необходимо указать '
                               'supplier_content_type: 9 (Завод) или 11 (Розничная сеть) '
                               'и supplier_id (id поставщика)',
                    'status': status.HTTP_400_BAD_REQUEST
                }
            )

        if supplier_id and not supplier_content_type:
            raise ValidationError(
                {
                    'message': 'Для создания связи с поставщиком необходимо указать '
                               'supplier_content_type: 9 (Завод) или 11 (Розничная сеть) '
                               'и supplier_id (id поставщика)',
                    'status': status.HTTP_400_BAD_REQUEST
                }
            )


