from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import StaffProfile, User, StudentProfile, AdminProfile
# from .models import FeeItem, FacultyCharge, ExtraCharge, Payment, Transaction

class CustomUserAdmin(UserAdmin):
    """
    Configuration for the User model in the Django admin.
    """
    model = User
    # Add 'role' to the fields displayed in the admin
    fieldsets = UserAdmin.fieldsets + (
        ('Role', {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role', {'fields': ('role',)}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'role')
    list_filter = ('role', 'is_staff', 'is_superuser', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)


admin.site.register(User, CustomUserAdmin)
admin.site.register(StudentProfile)
admin.site.register(AdminProfile)
admin.site.register(StaffProfile)
# admin.site.register(FeeItem)
# admin.site.register(FacultyCharge)
# admin.site.register(ExtraCharge)
# admin.site.register(Payment)
# admin.site.register(Transaction)
# This app uses the User model from 'accounts', which is already registered.