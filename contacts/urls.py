from django.urls import path
from . import views
from .apps import ContactsConfig


app_name = ContactsConfig.name


urlpatterns = [
    path('update/<int:pk>/', views.ContactUpdateAPIView.as_view(), name='update_contact'),
    ]
