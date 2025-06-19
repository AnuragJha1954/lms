from django.contrib import admin
from .models import TeacherProfile

@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'school', 'subject_specialization', 'phone_number',
        'qualification', 'experience_years'
    )
    search_fields = ('user__username', 'subject_specialization')
    list_filter = ('school', 'gender')
