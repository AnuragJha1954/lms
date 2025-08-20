from django.urls import path
from .views import add_topic_with_content, get_subjects_by_class, get_topics_with_contents_by_subject, get_teacher_notes_by_topic,create_chapter, get_classes_by_school

urlpatterns = [
    path('topic/add/', add_topic_with_content, name='add-topic-content'),
    path('subjects/', get_subjects_by_class, name='get-subjects-by-class'),
    path('topics-with-contents/', get_topics_with_contents_by_subject, name='topics-with-contents-by-subject'),
    path('topic/teacher-notes/', get_teacher_notes_by_topic, name='get-teacher-notes-by-topic'),
    path('subjects/<int:subject_id>/add-chapter/', create_chapter, name='create_chapter'),
    path('classes/<int:school_user_id>/', get_classes_by_school, name='get_classes_by_school'),
]
