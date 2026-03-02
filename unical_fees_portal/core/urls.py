from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FacultyViewSet, DepartmentViewSet

router = DefaultRouter()
router.register(r'faculties', FacultyViewSet)
router.register(r'departments', DepartmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]