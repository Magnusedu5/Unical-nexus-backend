from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .models import Applicant
from .serializers import ApplicantSerializer
from unical_fees_portal.accounts.permissions import IsAdmin
from unical_fees_portal.accounts.models import StudentProfile
import random
import string

User = get_user_model()

class ApplicantViewSet(viewsets.ModelViewSet):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    @action(detail=True, methods=['post'])
    def admit(self, request, pk=None):
        applicant = self.get_object()
        if applicant.status == 'ADMITTED':
            return Response({'detail': 'Applicant has already been admitted.'}, status=status.HTTP_400_BAD_REQUEST)

        # 1. Create a User account
        password = User.objects.make_random_password()
        username = f"{applicant.first_name.lower()}.{applicant.last_name.lower()}{''.join(random.choices(string.digits, k=3))}"
        
        if User.objects.filter(email=applicant.email).exists():
            return Response({'detail': 'A user with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            username=username,
            email=applicant.email,
            password=password,
            first_name=applicant.first_name,
            last_name=applicant.last_name,
            role=User.Roles.STUDENT
        )

        # 2. Create StudentProfile
        matric_number = f"24/CSC/{''.join(random.choices(string.digits, k=4))}"
        StudentProfile.objects.create(
            user=user,
            matric_number=matric_number,
            faculty=applicant.faculty,
            department=applicant.department,
            level=100
        )
        
        applicant.status = 'ADMITTED'
        applicant.save()

        return Response({
            'detail': 'Applicant admitted successfully.',
            'username': username,
            'matric_number': matric_number,
            'temp_password': password
        })