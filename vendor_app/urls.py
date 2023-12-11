from .views import VendorViewSet, PurchaseOrderViewSet
from django.urls import path, include
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'Vendors', VendorViewSet, basename='Vendor')
router.register(r'PurchaseOrder', PurchaseOrderViewSet,
                basename='PurchaseOrder')

urlpatterns = [
    path('api/', include(router.urls)),
]
