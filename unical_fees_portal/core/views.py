from rest_framework import viewsets, permissions
from .models import Faculty, Department
from .serializers import FacultySerializer, DepartmentSerializer
from unical_fees_portal.accounts.permissions import IsAdmin

class FacultyViewSet(viewsets.ModelViewSet):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]