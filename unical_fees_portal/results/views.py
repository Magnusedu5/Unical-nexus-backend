from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from .models import Result
from .serializers import ResultSerializer, ResultUploadSerializer
from .utils import process_result_csv
from unical_fees_portal.courses.models import Course
from unical_fees_portal.accounts.models import StudentProfile, User
from unical_fees_portal.accounts.permissions import IsAdmin, IsStudent, IsStaff

class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == User.Roles.STUDENT:
            return Result.objects.filter(student=user)
        return Result.objects.all()

    @action(detail=False, methods=['post'], parser_classes=[MultiPartParser, FormParser], permission_classes=[permissions.IsAuthenticated, IsAdmin | IsStaff])
    def upload(self, request):
        serializer = ResultUploadSerializer(data=request.data)
        if serializer.is_valid():
            course_id = serializer.validated_data['course_id']
            session = serializer.validated_data['session']
            semester = serializer.validated_data['semester']
            file = serializer.validated_data['file']

            course = get_object_or_404(Course, id=course_id)
            
            if not file.name.endswith('.csv'):
                 return Response({"error": "File must be a CSV."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                processed_count, errors = process_result_csv(file, course, session, semester)
                
                return Response({
                    "message": f"Successfully processed {processed_count} results.",
                    "errors": errors
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": f"Error processing file: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)