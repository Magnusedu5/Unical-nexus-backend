from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import CustomTokenObtainPairSerializer, UserSerializer
from .permissions import IsStudent, IsAdmin, IsStaff
from .models import User
from typing import Dict, Any

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom login view that uses the CustomTokenObtainPairSerializer.
    Returns access_token, refresh_token, user_role, user_id, and full_name.
    """
    serializer_class = CustomTokenObtainPairSerializer

class StudentDashboardView(APIView):
    """
    Protected GET endpoint for users with the 'STUDENT' role.
    Returns dummy data for the student dashboard.
    """
    permission_classes = [IsAuthenticated, IsStudent]

    def get(self, request, *args, **kwargs) -> Response:
        """
        Handles GET requests for the student dashboard.
        """
        data: Dict[str, Any] = {
            "message": "Welcome to your student dashboard.",
            "outstanding_fees": 50000.00,
            "course_registration_status": "Not Registered"
        }
        return Response(data)

class StaffDashboardView(APIView):
    """
    Protected GET endpoint for users with the 'STAFF' role.
    Returns dummy data for the staff dashboard.
    """
    permission_classes = [IsAuthenticated, IsStaff]

    def get(self, request, *args, **kwargs) -> Response:
        """
        Handles GET requests for the staff dashboard.
        """
        data: Dict[str, Any] = {
            "message": "Welcome to the staff dashboard.",
            "pending_verifications": 12,
            "uploaded_results": 45
        }
        return Response(data)

class AdminDashboardView(APIView):
    """
    Protected GET endpoint for users with the 'ADMIN' role.
    Returns dummy data for the admin dashboard.
    """
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request, *args, **kwargs) -> Response:
        """
        Handles GET requests for the admin dashboard.
        """
        data: Dict[str, Any] = {
            "message": "Welcome to the admin dashboard.",
            "total_revenue": 15000000.00,
            "total_students": 2500,
            "recent_transactions": 50
        }
        return Response(data)

class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing user instances.
    Only Admins should be able to access this.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]