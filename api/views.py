import csv
import io
from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Faculty, Department, Programme, Course, Student, Result, FeeItem, Session, Semester, Report
from .serializers import (
    FacultySerializer, 
    DepartmentSerializer, 
    CustomTokenObtainPairSerializer,
    ProgrammeSerializer,
    CourseSerializer,
    StudentSerializer,
    ResultSerializer,
    FeeItemSerializer,
    SessionSerializer,
    SemesterSerializer,
    UserSerializer,
    ReportSerializer
)

User = get_user_model()

class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class FacultyViewSet(viewsets.ModelViewSet):
    queryset = Faculty.objects.all().order_by('-created_at')
    serializer_class = FacultySerializer

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all().select_related('faculty').order_by('-created_at')
    serializer_class = DepartmentSerializer

class ProgrammeViewSet(viewsets.ModelViewSet):
    queryset = Programme.objects.all().select_related('department').order_by('-created_at')
    serializer_class = ProgrammeSerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all().select_related('programme').order_by('-created_at')
    serializer_class = CourseSerializer
    parser_classes = (MultiPartParser, FormParser)

    @action(detail=False, methods=['post'])
    def upload(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            with transaction.atomic():
                decoded_file = file.read().decode('utf-8')
                io_string = io.StringIO(decoded_file)
                reader = csv.DictReader(io_string)
                
                courses_created = 0
                errors = []
                for i, row in enumerate(reader, 1):
                    try:
                        programme_name = row['programme_name']
                        course_code = row['code']
                        course_name = row['name']
                    except KeyError as e:
                        raise ValueError(f"CSV is missing an expected column: {e}")

                    if not programme_name or not course_code or not course_name:
                        errors.append(f"Row {i}: 'programme_name', 'code', and 'name' cannot be empty.")
                        continue

                    programme = Programme.objects.filter(name__iexact=programme_name.strip()).first()
                    if programme:
                        _, created = Course.objects.get_or_create(
                            code=course_code.strip(),
                            programme=programme,
                            defaults={'name': course_name.strip()}
                        )
                        if created:
                            courses_created += 1
                    else:
                        errors.append(f"Row {i}: Programme '{programme_name}' not found.")
                
                if errors:
                    raise ValueError(f"Upload failed with {len(errors)} errors. Details: {'; '.join(errors)}")

            return Response({"message": f"Successfully created {courses_created} new courses."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all().select_related('department').order_by('-created_at')
    serializer_class = StudentSerializer

class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all().select_related('student', 'course').order_by('-created_at')
    serializer_class = ResultSerializer
    parser_classes = (MultiPartParser, FormParser)

    @action(detail=False, methods=['post'])
    def upload(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                decoded_file = file.read().decode('utf-8')
                io_string = io.StringIO(decoded_file)
                reader = csv.DictReader(io_string)
                results_processed = 0
                errors = []
                for i, row in enumerate(reader, 1):
                    try:
                        matric_number = row['matric_number']
                        course_code = row['course_code']
                        score = row['score']
                        grade = row['grade']
                    except KeyError as e:
                        raise ValueError(f"CSV is missing an expected column: {e}")

                    if not matric_number or not course_code:
                        errors.append(f"Row {i}: 'matric_number' and 'course_code' cannot be empty.")
                        continue

                    student = Student.objects.filter(matric_number=matric_number.strip()).first()
                    course = Course.objects.filter(code=course_code.strip()).first()
                    
                    if student and course:
                        Result.objects.update_or_create(
                            student=student,
                            course=course,
                            defaults={'score': score, 'grade': grade.strip()}
                        )
                        results_processed += 1
                    else:
                        if not student:
                            errors.append(f"Row {i}: Student with matric number '{matric_number}' not found.")
                        if not course:
                            errors.append(f"Row {i}: Course with code '{course_code}' not found.")
                
                if errors:
                    raise ValueError(f"Upload failed with {len(errors)} errors. Details: {'; '.join(errors)}")

            return Response({"message": f"Successfully uploaded/updated {results_processed} results."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class FeeItemViewSet(viewsets.ModelViewSet):
    queryset = FeeItem.objects.all().order_by('-created_at')
    serializer_class = FeeItemSerializer

class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all().order_by('-start_date')
    serializer_class = SessionSerializer

class SemesterViewSet(viewsets.ModelViewSet):
    queryset = Semester.objects.all().select_related('session').order_by('-start_date')
    serializer_class = SemesterSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all().order_by('-generated_at')
    serializer_class = ReportSerializer
