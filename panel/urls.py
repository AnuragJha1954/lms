from django.urls import path
from .views import (
    subject_list_create, subject_detail,
    chapter_list_create, chapter_detail,
    topic_list_create, topic_detail,
    content_list_create, content_detail,
    assign_students_to_subject
)

urlpatterns = [
    # Subject
    path("subjects/", subject_list_create, name="subject-list-create"),
    path("subjects/<int:pk>/", subject_detail, name="subject-detail"),

    # Chapter
    path("chapters/", chapter_list_create, name="chapter-list-create"),
    path("chapters/<int:pk>/", chapter_detail, name="chapter-detail"),

    # Topic
    path("topics/", topic_list_create, name="topic-list-create"),
    path("topics/<int:pk>/", topic_detail, name="topic-detail"),

    # Content
    path("contents/", content_list_create, name="content-list-create"),
    path("contents/<int:pk>/", content_detail, name="content-detail"),
    
    path("subjects/<int:subject_id>/assign-students/", assign_students_to_subject, name="assign-students-to-subject"),
]
