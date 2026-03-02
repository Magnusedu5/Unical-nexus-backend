from django.contrib import admin
from .models import Faculty, Department

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'faculty', 'created_at')
    list_filter = ('faculty',)
    search_fields = ('name', 'faculty__name')