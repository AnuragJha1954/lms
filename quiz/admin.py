from django.contrib import admin
from .models import Quiz, Question, Option, Answer, QuizAttempt, QuestionResponse


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'quiz_type', 'topic', 'teacher', 'is_active', 'created_at')
    list_filter = ('quiz_type', 'is_active')
    search_fields = ('title', 'description')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz', 'marks', 'is_multiple_choice', 'created_at')
    list_filter = ('quiz', 'is_multiple_choice')
    search_fields = ('text',)


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('text', 'question')
    list_filter = ('question',)
    search_fields = ('text',)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'option')
    list_filter = ('question',)


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('student', 'quiz', 'started_at', 'completed_at', 'score', 'is_submitted')
    list_filter = ('is_submitted', 'quiz')
    search_fields = ('student__user__full_name', 'quiz__title')


@admin.register(QuestionResponse)
class QuestionResponseAdmin(admin.ModelAdmin):
    list_display = ('attempt', 'question', 'is_correct')
    list_filter = ('is_correct', 'question')
    search_fields = ('attempt__student__user__full_name', 'question__text')
