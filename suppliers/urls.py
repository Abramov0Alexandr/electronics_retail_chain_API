from django.urls import path
from . import views
from .apps import SuppliersConfig


app_name = SuppliersConfig.name


urlpatterns = [
    path('create/', views.FactoryCreateApiView.as_view(), name='create_factory'),
    path('list/', views.FactoryListAPIView.as_view(), name='factory_list'),
    path('delete/<int:pk>/', views.DeleteFactoryAPIView.as_view(), name='delete_factory'),
    ]
