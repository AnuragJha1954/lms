from django.contrib import admin
from .models import (
    ClassModel, Subject, TeacherSubjectAssignment,
    Chapter, Topic, Content
)

@admin.register(ClassModel)
class ClassModelAdmin(admin.ModelAdmin):
    list_display = ('class_name', 'section', 'school', 'academic_year')
    search_fields = ('class_name', 'section')
    list_filter = ('school', 'academic_year')


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'class_model')
    search_fields = ('name', 'code')
    list_filter = ('class_model',)


@admin.register(TeacherSubjectAssignment)
class TeacherSubjectAssignmentAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'subject', 'assigned_on')
    search_fields = ('teacher__user__username', 'subject__name')
    list_filter = ('assigned_on',)


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('title', 'number', 'subject')
    search_fields = ('title',)
    list_filter = ('subject',)


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'number', 'chapter', 'is_completed')
    search_fields = ('title',)
    list_filter = ('chapter', 'is_completed')


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'topic', 'order', 'is_active', 'is_completed', 'created_at')
    search_fields = ('title',)
    list_filter = ('topic', 'is_active', 'is_completed')
