from rest_framework import viewsets, permissions
from .models import Course
from .serializers import CourseSerializer
from unical_fees_portal.accounts.permissions import IsAdmin

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    # Allow all authenticated users to view, but only admins to edit
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # For stricter control where only admins can write:
    # permission_classes = [permissions.IsAuthenticated, IsAdmin] 