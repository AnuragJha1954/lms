from django.contrib import admin
from .models import SchoolProfile

@admin.register(SchoolProfile)
class SchoolProfileAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'user', 'registration_number', 'phone_number',
        'board_affiliation', 'principal_name', 'established_year'
    )
    search_fields = ('name', 'registration_number', 'user__username')
    list_filter = ('board_affiliation', 'established_year')
