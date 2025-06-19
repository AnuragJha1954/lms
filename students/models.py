from django.db import models
from users.models import CustomUser
from school.models import SchoolProfile

class StudentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='student_profile')
    school = models.ForeignKey(SchoolProfile, on_delete=models.CASCADE, related_name='students')
    roll_number = models.CharField(max_length=50)
    guardian_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=20)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(
        max_length=10,
        choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')],
        blank=True,
        null=True
    )
    address = models.TextField(blank=True, null=True)
    admission_date = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='student_profiles/', blank=True, null=True)

    def __str__(self):
        return self.user.full_name




class StudentClassAssignment(models.Model):
    student = models.OneToOneField(StudentProfile, on_delete=models.CASCADE, related_name='class_assignment')
    class_model = models.ForeignKey('v1.ClassModel', on_delete=models.CASCADE, related_name='students')
    assigned_date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'class_model')

    def __str__(self):
        return f"{self.student.user.full_name} → {self.class_model}"





class TopicProgress(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='topic_progress')
    topic = models.ForeignKey('v1.Topic', on_delete=models.CASCADE, related_name='progress')
    is_completed = models.BooleanField(default=False)
    completion_percentage = models.FloatField(default=0.0)
    last_accessed = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'topic')

    def __str__(self):
        return f"{self.student.user.full_name} → {self.topic.title} [{self.completion_percentage}%]"





class ContentProgress(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='content_progress')
    content = models.ForeignKey('v1.Content', on_delete=models.CASCADE, related_name='progress')
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('student', 'content')

    def __str__(self):
        return f"{self.student.user.full_name} → {self.content.title} ({'✓' if self.is_completed else '✗'})"







class StudentLoginActivity(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='login_activities')
    login_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.full_name} logged in at {self.login_time}"






class TopicAccessLog(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='topic_access_logs')
    topic = models.ForeignKey('v1.Topic', on_delete=models.CASCADE, related_name='access_logs')
    accessed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.full_name} accessed {self.topic.title} at {self.accessed_at}"



