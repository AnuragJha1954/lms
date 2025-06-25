from django.urls import path
from .views import register_school,update_teacher, delete_teacher,update_student, delete_student,add_class_with_subjects,assign_teacher_to_subject, assign_student_to_class, manage_school_profile

urlpatterns = [
    path('register/', register_school, name='register-school'),
    path('<int:school_id>/teachers/<int:teacher_id>/update/', update_teacher, name='update-teacher'),
    path('<int:school_id>/teachers/<int:teacher_id>/delete/', delete_teacher, name='delete-teacher'),
    path('<int:school_id>/students/<int:student_id>/update/', update_student, name='update-student'),
    path('<int:school_id>/students/<int:student_id>/delete/', delete_student, name='delete-student'),
    path('class/add/<int:school_user_id>/', add_class_with_subjects, name='add-class-subjects'),
    path('subject/assign-teacher/', assign_teacher_to_subject, name='assign-teacher-subject'),
    path('class/assign-student/', assign_student_to_class, name='assign-student-class'),
    path('profile/<int:school_user_id>/', manage_school_profile, name='school-profile'),
]
