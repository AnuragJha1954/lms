# v1/admin.py
from django.contrib import admin
from .models import ClassModel, Subject, TeacherSubjectAssignment, Chapter, Topic, Content


class ContentInline(admin.TabularInline):
    model = Content
    extra = 1
    fields = ("title", "order", "is_active", "is_completed")
    ordering = ("order",)


class TopicInline(admin.TabularInline):
    model = Topic
    extra = 1
    fields = ("title", "number", "is_completed")
    ordering = ("number",)


class ChapterInline(admin.TabularInline):
    model = Chapter
    extra = 1
    fields = ("title", "number")
    ordering = ("number",)


@admin.register(ClassModel)
class ClassModelAdmin(admin.ModelAdmin):
    list_display = ("class_name", "section", "academic_year", "school")
    list_filter = ("academic_year", "school")
    search_fields = ("class_name", "section", "school__name")
    ordering = ("school", "class_name", "section")


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "student")
    list_filter = ("student",)
    search_fields = ("name", "code", "student__user__full_name")
    inlines = [ChapterInline]


@admin.register(TeacherSubjectAssignment)
class TeacherSubjectAssignmentAdmin(admin.ModelAdmin):
    list_display = ("subject", "teacher", "assigned_on")
    list_filter = ("assigned_on", "teacher")
    search_fields = ("subject__name", "teacher__user__full_name")
    autocomplete_fields = ("subject", "teacher")


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ("title", "number", "subject")
    list_filter = ("subject",)
    search_fields = ("title", "subject__name")
    ordering = ("subject", "number")
    inlines = [TopicInline]


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("title", "number", "chapter", "is_completed")
    list_filter = ("chapter", "is_completed")
    search_fields = ("title", "chapter__title")
    ordering = ("chapter", "number")
    inlines = [ContentInline]


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ("title", "topic", "order", "is_active", "is_completed", "created_at")
    list_filter = ("is_active", "is_completed", "topic")
    search_fields = ("title", "topic__title")
    ordering = ("topic", "order")
