from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter

# A router for endpoints that don't fit a natural app-based prefix
root_router = DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # Authentication and dashboard endpoints
    path('api/', include('unical_fees_portal.accounts.urls')),

    # App URLs
    path('fees/', include('unical_fees_portal.fees.urls')),
    path('students/', include('unical_fees_portal.students.urls')),
    path('staff/', include('unical_fees_portal.staff.urls')),
    path('admissions/', include('unical_fees_portal.admissions.urls')),
    path('courses/', include('unical_fees_portal.courses.urls')),
    path('hostels/', include('unical_fees_portal.hostels.urls')),
    path('results/', include('unical_fees_portal.results.urls')),
    path('settings/', include('unical_fees_portal.portal_settings.urls')),
    path('', include('unical_fees_portal.core.urls')), # For faculties and departments

    # Root Router
    path('', include(root_router.urls)),
]
