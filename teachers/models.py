from django.db import models
from users.models import CustomUser
from school.models import SchoolProfile



class TeacherProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='teacher_profile')
    school = models.ForeignKey(SchoolProfile, on_delete=models.CASCADE, related_name='teachers')
    subject_specialization = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    qualification = models.CharField(max_length=255)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    experience_years = models.PositiveIntegerField(default=0)
    profile_picture = models.ImageField(upload_to='teacher_profiles/', blank=True, null=True)
    assigned_classes = models.ManyToManyField(
        'v1.ClassModel',
        related_name='assigned_teachers'
    )

    def __str__(self):
        return self.user.full_name






class TeacherNote(models.Model):
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, related_name='notes')
    topic = models.ForeignKey('v1.Topic', on_delete=models.CASCADE, related_name='teacher_notes')
    note_text = models.TextField(blank=True, null=True)
    note_file = models.FileField(upload_to='teacher_notes/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Note by {self.teacher.user.full_name} on {self.topic.title}"
