from django.db import models
from users.models import CustomUser

class SchoolProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='school_profile')
    name = models.CharField(max_length=255)
    address = models.TextField()
    phone_number = models.CharField(max_length=20)
    registration_number = models.CharField(max_length=100, unique=True)
    board_affiliation = models.CharField(max_length=100, blank=True, null=True)
    principal_name = models.CharField(max_length=255, blank=True, null=True)
    established_year = models.PositiveIntegerField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to='school_logos/', blank=True, null=True)

    def __str__(self):
        return self.name
