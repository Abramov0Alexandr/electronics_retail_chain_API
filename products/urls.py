from django.urls import path
from . import views
from .apps import ProductsConfig

app_name = ProductsConfig.name


urlpatterns = [
    path('create/', views.ProductCreateAPIView.as_view(), name='create_product'),
    path('list/', views.ProductListAPIView.as_view(), name='product_list'),
    path('update/<int:pk>/', views.ProductUpdateAPIView.as_view(), name='update_product'),
    path('delete/<int:pk>/', views.ProductDeleteAPIView.as_view(), name='delete_product'),
    ]
