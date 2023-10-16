from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


schema_view = get_schema_view(
   openapi.Info(
      title="Marketplace API template",
      default_version='v1',
      description="Here you can find all the information about requests and check them",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(url="https://github.com/Abramov0Alexandr"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/employee/', include('employees.urls', namespace='employees')),
    path('api/', include('suppliers.urls', namespace='supplier_urls')),
    path('api/products/', include('products.urls', namespace='products')),
    path('api/contacts/', include('contacts.urls', namespace='contacts')),

    # authorization urls
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # documentation
    path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
