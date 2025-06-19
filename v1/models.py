from django.db import models
from school.models import SchoolProfile
from teachers.models import TeacherProfile

class ClassModel(models.Model):
    school = models.ForeignKey(SchoolProfile, on_delete=models.CASCADE, related_name='classes')
    class_name = models.CharField(max_length=20)  # e.g., 'Class 10', 'Grade 6'
    section = models.CharField(max_length=10)     # e.g., 'A', 'B'
    academic_year = models.CharField(max_length=20)  # e.g., '2024-2025'

    class Meta:
        unique_together = ('school', 'class_name', 'section', 'academic_year')

    def __str__(self):
        return f"{self.class_name}-{self.section} ({self.academic_year})"




class Subject(models.Model):
    class_model = models.ForeignKey(ClassModel, on_delete=models.CASCADE, related_name='subjects')
    name = models.CharField(max_length=100)  # e.g., 'Mathematics', 'Science'
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.class_model})"






class TeacherSubjectAssignment(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='assigned_teachers')
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, related_name='subject_assignments')
    assigned_on = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('subject', 'teacher')

    def __str__(self):
        return f"{self.teacher.user.full_name} → {self.subject.name} ({self.subject.class_model})"






class Chapter(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='chapters')
    title = models.CharField(max_length=255)
    number = models.PositiveIntegerField()  # e.g., Chapter 1, 2, etc.
    description = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('subject', 'number')
        ordering = ['number']

    def __str__(self):
        return f"Chapter {self.number}: {self.title} ({self.subject.name})"




class Topic(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='topics')
    title = models.CharField(max_length=255)
    number = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)  # ❗ global completion

    class Meta:
        unique_together = ('chapter', 'number')
        ordering = ['number']

    def __str__(self):
        return f"Topic {self.number}: {self.title} ({self.chapter.title})"




class Content(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='contents')
    title = models.CharField(max_length=255)
    video_link = models.URLField(blank=True, null=True)
    text_content = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    is_completed = models.BooleanField(default=False)  # ❗ global completion
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.title} ({self.topic.title})"


