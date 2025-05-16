from django.contrib import admin
from .models import (
    Class, 
    Subject, 
    Chapter, 
    Topic, 
    Content
)

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('class_name', 'section', 'school')
    search_fields = ('class_name', 'section', 'school__name')
    list_filter = ('school',)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'assigned_class', 'assigned_teacher')
    search_fields = ('name', 'assigned_class__class_name', 'assigned_teacher__name')
    list_filter = ('assigned_class', 'assigned_teacher')


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject')
    search_fields = ('name', 'subject__name')
    list_filter = ('subject',)


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'chapter')
    search_fields = ('name', 'chapter__name')
    list_filter = ('chapter',)


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('topic', 'content_link', 'completed')
    search_fields = ('topic__name', 'content_link')
    list_filter = ('completed',)
