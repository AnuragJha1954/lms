from django.urls import path
from students import views
from .views import create_student, mark_content_progress, mark_topic_progress, get_last_accessed_topics, store_student_login, get_last_login_info, manage_student_profile

urlpatterns = [
    path('create/<int:school_user_id>', create_student, name='create-student'),
    path('progress/content/', mark_content_progress, name='mark-content-progress'),
    path('progress/topic/', mark_topic_progress, name='mark-topic-progress'),
    path('last-accessed/<int:student_id>/', get_last_accessed_topics, name='last-accessed-topics'),
    path('login-activity/<int:student_id>/', store_student_login, name='store-student-login'),
    path('last-login/<int:student_id>/', get_last_login_info, name='get-last-login'),
    path('profile/<int:student_id>/', manage_student_profile, name='manage-student-profile'),
    path("dashboard/", views.student_dashboard, name="student-dashboard"),
    path("subjects/<int:subject_id>/chapters/", views.get_chapters_of_subject, name="get-chapters-of-subject"),
    path("chapters/<int:chapter_id>/topics/", views.get_topics_of_chapter, name="get-topics-of-chapter"),
    path("topics/<int:topic_id>/contents/", views.get_content_of_topic, name="get-content-of-topic"),
    path("chapters/<int:chapter_id>/topics-with-contents/", views.get_topics_with_content_for_chapter, name="get-topics-with-content-for-chapter"),

]
