from django.contrib import admin
from .models import (
    StudentSchool,
    StudentProfile,
    AssignedChapterTopic,
    TopicProgress
)

@admin.register(StudentSchool)
class StudentSchoolAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'user', 'class_assigned', 'school')
    search_fields = ('student_name', 'user__email', 'school__name')
    list_filter = ('class_assigned', 'school')


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('student_school', 'dob', 'phone', 'gender', 'guardian_name')
    search_fields = ('student_school__student_name', 'guardian_name', 'phone')
    list_filter = ('gender', 'class_assigned')


@admin.register(AssignedChapterTopic)
class AssignedChapterTopicAdmin(admin.ModelAdmin):
    list_display = ('student', 'chapter')
    search_fields = ('student__student_name', 'chapter__name')
    filter_horizontal = ('topics',)


@admin.register(TopicProgress)
class TopicProgressAdmin(admin.ModelAdmin):
    list_display = ('student', 'topic', 'completion_percentage', 'is_completed', 'last_accessed')
    search_fields = ('student__email', 'topic__name')
    list_filter = ('is_completed', 'last_accessed')