from django.urls import path
from .views import create_teacher, get_teacher_students, mark_content_completed, mark_topic_completed, add_teacher_note,get_teachers_by_school

urlpatterns = [
    path('create-teacher/<int:school_user_id>/', create_teacher, name='create_teacher'),
    path('teacher-students/<int:teacher_user_id>/', get_teacher_students, name='get_teacher_students'),
    path('add-note/<int:teacher_user_id>/', add_teacher_note, name='add_teacher_note'),
    path('mark-content-completed/', mark_content_completed, name='mark_content_completed'),
    path('mark-topic-completed/', mark_topic_completed, name='mark_topic_completed'),
    path('get-teachers/<int:school_user_id>/', get_teachers_by_school, name='get-teachers-by-school'),
]
