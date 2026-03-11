
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomTokenObtainPairView, StudentDashboardView, AdminDashboardView, StaffDashboardView, UserViewSet
from .views import CustomTokenObtainPairView, StudentDashboardView, AdminDashboardView, StaffDashboardView
from rest_framework_simplejwt.views import TokenRefreshView
from .views import StudentViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'', StudentViewSet, basename='student')

urlpatterns = [
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('dashboard/student/', StudentDashboardView.as_view(), name='student_dashboard'),
    path('dashboard/staff/', StaffDashboardView.as_view(), name='staff_dashboard'),
    path('dashboard/admin/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('', include(router.urls)),
]
