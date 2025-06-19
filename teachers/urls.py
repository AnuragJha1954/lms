from django.urls import path
from .views import create_teacher, get_teacher_students, mark_content_completed, mark_topic_completed, add_teacher_note

urlpatterns = [
    path('create-teacher/', create_teacher, name='create_teacher'),
    path('teacher-students/', get_teacher_students, name='get_teacher_students'),
    path('add-note/', add_teacher_note, name='add_teacher_note'),
    path('mark-content-completed/', mark_content_completed, name='mark_content_completed'),
    path('mark-topic-completed/', mark_topic_completed, name='mark_topic_completed'),
]
