from rest_framework import viewsets, permissions
from unical_fees_portal.accounts.models import User
from .serializers import StudentSerializer
from unical_fees_portal.accounts.permissions import IsAdmin

class StudentViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(role=User.Roles.STUDENT)
    serializer_class = StudentSerializer
    # Only admins can manage student accounts
    permission_classes = [permissions.IsAuthenticated, IsAdmin]