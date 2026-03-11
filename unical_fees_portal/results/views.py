import csv
import io
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.db import transaction
from django.shortcuts import get_object_or_404
from .models import Result
from .serializers import ResultSerializer, ResultUploadSerializer
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
                decoded_file = file.read().decode('utf-8')
                io_string = io.StringIO(decoded_file)
                reader = csv.DictReader(io_string)
                
                processed_count = 0
                errors = []

                with transaction.atomic():
                    for index, row in enumerate(reader):
                        # Expected CSV format: matric_number, score, grade
                        matric_number = row.get('matric_number')
                        score = row.get('score')
                        grade = row.get('grade')
                        
                        if not matric_number or not score:
                            errors.append(f"Row {index + 1}: Missing matric_number or score")
                            continue

                        try:
                            student_profile = StudentProfile.objects.get(matric_number=matric_number.strip())
                            student = student_profile.user
                            
                            Result.objects.update_or_create(
                                student=student,
                                course=course,
                                session=session,
                                semester=semester,
                                defaults={
                                    'score': score,
                                    'grade': grade
                                }
                            )
                            processed_count += 1
                        except StudentProfile.DoesNotExist:
                            errors.append(f"Row {index + 1}: Student with matric {matric_number} not found")
                
                return Response({
                    "message": f"Successfully processed {processed_count} results.",
                    "errors": errors
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": f"Error processing file: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)