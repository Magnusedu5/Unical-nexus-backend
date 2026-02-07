
from django.urls import path
from .views import CustomTokenObtainPairView, StudentDashboardView, AdminDashboardView, StaffDashboardView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('dashboard/student/', StudentDashboardView.as_view(), name='student_dashboard'),
    path('dashboard/staff/', StaffDashboardView.as_view(), name='staff_dashboard'),
    path('dashboard/admin/', AdminDashboardView.as_view(), name='admin_dashboard'),
]
