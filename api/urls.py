from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CustomLoginView, 
    FacultyViewSet, 
    DepartmentViewSet, 
    ProgrammeViewSet, 
    CourseViewSet, 
    StudentViewSet, 
    ResultViewSet, 
    FeeItemViewSet,
    SessionViewSet,
    SemesterViewSet,
    UserViewSet,
    ReportViewSet
)

router = DefaultRouter()
router.register(r'faculties', FacultyViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'programmes', ProgrammeViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'students', StudentViewSet)
router.register(r'results', ResultViewSet)
router.register(r'fee-items', FeeItemViewSet)
router.register(r'sessions', SessionViewSet)
router.register(r'semesters', SemesterViewSet)
router.register(r'users', UserViewSet)
router.register(r'reports', ReportViewSet)

urlpatterns = [
    path('auth/login/', CustomLoginView.as_view(), name='auth_login'),
    path('', include(router.urls)),
]