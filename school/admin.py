from django.contrib import admin
from .models import School

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'email', 'phone')
    search_fields = ('name', 'email', 'phone', 'user__email')
    list_filter = ('name',)
