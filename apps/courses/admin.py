from django.contrib import admin
from .models import Course, CourseTeacher, CourseStudent


class CourseTeacherInline(admin.TabularInline):
    model = CourseTeacher
    extra = 1
    autocomplete_fields = ["user"]


class CourseStudentInline(admin.TabularInline):
    model = CourseStudent
    extra = 1
    autocomplete_fields = ["user"]


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "primary_owner", "created_at", "updated_at")
    search_fields = ("name", "description")
    list_filter = ("created_at", "updated_at")
    inlines = [CourseTeacherInline, CourseStudentInline]
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('primary_owner')


@admin.register(CourseTeacher)
class CourseTeacherAdmin(admin.ModelAdmin):
    list_display = ("course", "user", "added_at")
    search_fields = ("course__name", "user__email", "user__first_name", "user__last_name")
    list_filter = ("added_at",)
    autocomplete_fields = ("course", "user")
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('course', 'user')


@admin.register(CourseStudent)
class CourseStudentAdmin(admin.ModelAdmin):
    list_display = ("course", "user", "enrolled_at")
    search_fields = ("course__name", "user__email", "user__first_name", "user__last_name")
    list_filter = ("enrolled_at",)
    autocomplete_fields = ("course", "user")
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('course', 'user')
