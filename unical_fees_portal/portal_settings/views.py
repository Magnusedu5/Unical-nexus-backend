from rest_framework import viewsets, mixins, permissions
from .models import PortalSettings
from .serializers import PortalSettingsSerializer
from unical_fees_portal.accounts.permissions import IsAdmin

class PortalSettingsViewSet(mixins.ListModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = PortalSettings.objects.all()
    serializer_class = PortalSettingsSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def list(self, request, *args, **kwargs):
        # Ensure one setting object exists
        if not PortalSettings.objects.exists():
            PortalSettings.objects.create()
        return super().list(request, *args, **kwargs)
        
    def get_object(self):
        if not PortalSettings.objects.exists():
            return PortalSettings.objects.create()
        return PortalSettings.objects.first()