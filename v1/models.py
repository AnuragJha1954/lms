from django.db import models

from school.models import (
    School
)

from teachers.models import (
    Teacher
)

class Class(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    class_name = models.CharField(max_length=50)
    section = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.class_name} - {self.section}"
    
    
    


class Subject(models.Model):
    name = models.CharField(max_length=100)
    assigned_teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
    assigned_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name




class Chapter(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name





class Topic(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name






class Content(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    content_link = models.URLField()
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)  # New field

    def __str__(self):
        return f"Content for {self.topic.name}"





