from django.urls import path
from .views import PortalSettingsViewSet

urlpatterns = [
    path('', PortalSettingsViewSet.as_view({
        'get': 'list',
        'put': 'update',
        'patch': 'partial_update'
    }), name='settings'),
]