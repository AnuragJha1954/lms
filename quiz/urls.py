from django.urls import path
from .views import create_quiz, get_quizzes_by_topic, submit_quiz_attempt,get_teacher_quizzes_by_topic,get_quiz_detail_with_questions

urlpatterns = [
    path('create/<int:topic_id>/', create_quiz),
    path('create/<int:topic_id>/teacher/<int:teacher_id>/', create_quiz),
    path('submit/<int:student_id>/', submit_quiz_attempt),
    path('topic-quizzes/<int:topic_id>/', get_quizzes_by_topic),
    path('teacher-quizzes/<int:teacher_id>/<int:topic_id>/', get_teacher_quizzes_by_topic),
    path('quiz-detail/<int:quiz_id>/', get_quiz_detail_with_questions),
]
