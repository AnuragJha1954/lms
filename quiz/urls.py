from django.urls import path
from .views import create_quiz, get_quizzes_by_topic, submit_quiz_attempt,get_teacher_quizzes_by_topic,get_quiz_detail_with_questions,get_quizzes_for_student, get_all_quizzes, update_quiz, delete_quiz

urlpatterns = [
    path('create/<int:topic_id>/', create_quiz),
    path('create/<int:topic_id>/teacher/<int:teacher_id>/', create_quiz),
    path('submit/<int:student_id>/', submit_quiz_attempt),
    path('topic-quizzes/<int:topic_id>/', get_quizzes_by_topic),
    path('teacher-quizzes/<int:teacher_id>/<int:topic_id>/', get_teacher_quizzes_by_topic),
    path('quiz-detail/<int:quiz_id>/', get_quiz_detail_with_questions),
    path('quizzes/<int:student_id>/', get_quizzes_for_student, name='get_quizzes_for_student'),
    path('get-all-quizzes/', get_all_quizzes, name='get_all_quizzes'),
    path('quizzes/<int:quiz_id>/', update_quiz, name='update_quiz'),
    path('quizzes/<int:quiz_id>/delete/', delete_quiz, name='delete_quiz'),
]
