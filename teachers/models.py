from django.db import models
from users.models import CustomUser
from school.models import School

class Teacher(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.name