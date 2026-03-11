from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import viewsets
from rest_framework.views import APIView
import random
import string
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import CustomTokenObtainPairSerializer, UserSerializer
from .serializers import CustomTokenObtainPairSerializer
from .permissions import IsStudent, IsAdmin, IsStaff
from .models import User
from typing import Dict, Any
from unical_fees_portal.accounts.models import User
from unical_fees_portal.accounts.serializers import UserSerializer
from .models import Applicant
from .serializers import ApplicantSerializer
from unical_fees_portal.accounts.permissions import IsAdmin
from unical_fees_portal.accounts.models import User, StudentProfile

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

    def get(self, request, *args, **kwargs):
        data = {
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

    def get(self, request, *args, **kwargs):
        data = {
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

    def get(self, request, *args, **kwargs):
        data = {
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
    permission_classes = [permissions.IsAuthenticated, IsAdmin]