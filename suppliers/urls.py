from django.urls import path
from . import views
from .apps import SuppliersConfig


app_name = SuppliersConfig.name


urlpatterns = [
    # Эндпоинты для модели Factory
    path('factories/create/', views.FactoryCreateApiView.as_view(), name='create_factory'),
    path('factories/list/', views.FactoryListAPIView.as_view(), name='factory_list'),
    path('factories/update/<int:pk>/', views.FactoryUpdateAPIView.as_view(), name='update_factory'),
    path('factories/delete/<int:pk>/', views.FactoryDeleteAPIView.as_view(), name='delete_factory'),

    # Эндпоинты для модели RetailChains
    path('retail_chain/create/', views.RetailChainCreateApiView.as_view(), name='create_retail_chain'),
    path('retail_chain/list/', views.RetailChainListApiView.as_view(), name='list_retail_chain'),
    path('retail_chain/update/<int:pk>/', views.RetailChainUpdateAPIView.as_view(), name='update_retail_chain'),
    path('retail_chain/delete/<int:pk>/', views.RetailChainDeleteAPIView.as_view(), name='delete_retail_chain'),

    # Эндпоинты для модели Vendor
    path('vendor/create/', views.VendorCreateAPIView.as_view(), name='create_vendor'),
    path('vendor/list/', views.VendorsListAPIView.as_view(), name='vendors_list'),
    path('vendor/update/<int:pk>/', views.VendorUpdateAPIView.as_view(), name='update_vendor'),
    path('vendor/delete/<int:pk>/', views.VendorDeleteAPIView.as_view(), name='delete_vendor'),
]
