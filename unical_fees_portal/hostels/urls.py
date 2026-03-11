from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HostelRequestViewSet, HostelViewSet

router = DefaultRouter()
router.register(r'list', HostelViewSet)
router.register(r'requests', HostelRequestViewSet)

urlpatterns = [
    path('', include(router.urls)),
]