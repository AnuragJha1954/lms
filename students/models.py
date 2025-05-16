from django.db import models
from django.utils import timezone
from users.models import CustomUser
from v1.models import (
    Class,
    Chapter,
    Topic,
    Subject
)
from school.models import School

class StudentSchool(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    student_name = models.CharField(max_length=255)
    class_assigned = models.ForeignKey(Class, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    def __str__(self):
        return self.student_name
    
    


class StudentProfile(models.Model):
    student_school = models.ForeignKey(StudentSchool, on_delete=models.CASCADE)
    class_assigned = models.ForeignKey(Class, on_delete=models.CASCADE)
    dob = models.DateField()
    address = models.TextField()
    phone = models.CharField(max_length=20)
    gender = models.CharField(max_length=10)
    guardian_name = models.CharField(max_length=255)
    emergency_contact = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.student_school.student_name}'s Profile"
    
    

class AssignedChapterTopic(models.Model):
    student = models.ForeignKey(StudentSchool, on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    topics = models.ManyToManyField(Topic)

    def __str__(self):
        return f"{self.student.student_name} - {self.chapter.name}"




class TopicProgress(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    completion_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    last_accessed = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('student', 'topic')

    def __str__(self):
        return f"{self.student.full_name} - {self.topic.name} - {self.completion_percentage}%"