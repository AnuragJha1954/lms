from django.contrib import admin
from .models import (
    StudentProfile, StudentClassAssignment, TopicProgress,
    ContentProgress, StudentLoginActivity, TopicAccessLog
)

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'school', 'roll_number', 'contact_number', 'admission_date')
    search_fields = ('user__username', 'roll_number')
    list_filter = ('school', 'gender', 'admission_date')


@admin.register(StudentClassAssignment)
class StudentClassAssignmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'class_model', 'assigned_date')
    search_fields = ('student__user__username',)
    list_filter = ('class_model',)


@admin.register(TopicProgress)
class TopicProgressAdmin(admin.ModelAdmin):
    list_display = ('student', 'topic', 'completion_percentage', 'is_completed', 'last_accessed')
    search_fields = ('student__user__username', 'topic__title')
    list_filter = ('is_completed',)


@admin.register(ContentProgress)
class ContentProgressAdmin(admin.ModelAdmin):
    list_display = ('student', 'content', 'is_completed', 'completed_at')
    search_fields = ('student__user__username', 'content__title')
    list_filter = ('is_completed',)


@admin.register(StudentLoginActivity)
class StudentLoginActivityAdmin(admin.ModelAdmin):
    list_display = ('student', 'login_time')
    search_fields = ('student__user__username',)
    list_filter = ('login_time',)


@admin.register(TopicAccessLog)
class TopicAccessLogAdmin(admin.ModelAdmin):
    list_display = ('student', 'topic', 'accessed_at')
    search_fields = ('student__user__username', 'topic__title')
    list_filter = ('accessed_at',)
