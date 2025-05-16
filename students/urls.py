from django.urls import path
from students import views

urlpatterns = [
    # Profile CRUD Operations Urls
    path('profile/<int:user_id>/', views.get_student_profile, name='get_student_profile'),
    path('profile/<int:user_id>/create/', views.create_student_profile, name='create_student_profile'),
    path('profile/<int:user_id>/update/', views.update_student_profile, name='update_student_profile'),
    path('profile/<int:user_id>/delete/', views.delete_student_profile, name='delete_student_profile'),
    
    # Dashboard related Urls
    path('dashboard/<int:user_id>/<str:account_type>/', views.student_dashboard),
     
    # Urls to get the subjects of the student class
    path('subjects/<int:user_id>/', views.get_student_subjects),
    
    #Urls to get the chapters and the topics assigned
    path('chapters/<int:subject_id>/', views.get_subject_chapters_with_progress),
]
