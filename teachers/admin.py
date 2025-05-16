from django.contrib import admin
from .models import Teacher

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'school', 'email', 'phone')
    search_fields = ('name', 'email', 'phone', 'user__email', 'school__name')
    list_filter = ('school',)
