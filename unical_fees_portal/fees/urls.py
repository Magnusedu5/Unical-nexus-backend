from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    FeeItemViewSet, FacultyChargeViewSet, ExtraChargeViewSet, 
    PaymentViewSet, TransactionViewSet
)

router = DefaultRouter()
router.register(r'items', FeeItemViewSet)
router.register(r'faculty-charges', FacultyChargeViewSet)
router.register(r'extra-charges', ExtraChargeViewSet)
router.register(r'payments', PaymentViewSet) # Note: user requested /payments/
router.register(r'transactions', TransactionViewSet) # Note: user requested /transactions/

urlpatterns = [
    path('', include(router.urls)),
]