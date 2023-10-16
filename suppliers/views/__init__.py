__all__ = [
    'FactoryCreateApiView',
    'FactoryListAPIView',
    'FactoryUpdateAPIView',
    'FactoryDeleteAPIView',
    'RetailChainCreateApiView',
    'RetailChainListApiView',
    'RetailChainUpdateAPIView',
    'RetailChainDeleteAPIView',
    'VendorCreateAPIView',
    'VendorsListAPIView',
    'VendorUpdateAPIView',
    'VendorDeleteAPIView',
    ]


from .factory_views import FactoryCreateApiView, FactoryListAPIView, FactoryUpdateAPIView, FactoryDeleteAPIView
from .retail_chain_views import (RetailChainCreateApiView, RetailChainListApiView,
                                 RetailChainUpdateAPIView, RetailChainDeleteAPIView)
from .vendor_views import VendorCreateAPIView, VendorsListAPIView, VendorUpdateAPIView, VendorDeleteAPIView
