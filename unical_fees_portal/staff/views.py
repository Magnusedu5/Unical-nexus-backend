from rest_framework import viewsets, permissions
from unical_fees_portal.accounts.models import User
from .serializers import StaffSerializer
from unical_fees_portal.accounts.permissions import IsAdmin

class StaffViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(role=User.Roles.STAFF)
    serializer_class = StaffSerializer
    # Only admins can manage staff accounts
    permission_classes = [permissions.IsAuthenticated, IsAdmin]