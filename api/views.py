from rest_framework import viewsets
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

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all().select_related('department').order_by('-created_at')
    serializer_class = StudentSerializer

class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all().select_related('student', 'course').order_by('-created_at')
    serializer_class = ResultSerializer

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
