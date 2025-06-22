from django.db import models
from django.core.exceptions import ValidationError
from users.models import CustomUser
from students.models import StudentProfile
from v1.models import Topic

class Quiz(models.Model):
    QUIZ_TYPE_CHOICES = [
        ('topic', 'Topic Quiz'),
        ('teacher', 'Teacher Quiz'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    quiz_type = models.CharField(max_length=10, choices=QUIZ_TYPE_CHOICES)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='quizzes', null=True, blank=True)
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='teacher_quizzes', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def clean(self):
        if self.quiz_type == 'topic' and not self.topic:
            raise ValidationError("Topic is required for Topic Quiz.")
        if self.quiz_type == 'teacher' and (not self.topic or not self.teacher):
            raise ValidationError("Both Topic and Teacher are required for Teacher Quiz.")
        if self.teacher and self.teacher.role != 'teacher':
            raise ValidationError("Assigned user must have the teacher role.")

    def save(self, *args, **kwargs):
        self.full_clean()  # enforce validation
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.get_quiz_type_display()})"
    
    

class Question(models.Model):
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    marks = models.FloatField(default=1.0)
    is_multiple_choice = models.BooleanField(default=False)  # supports multiple correct answers
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Q: {self.text[:50]}..."

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=255)

    def __str__(self):
        return f"Option: {self.text[:50]} (Q: {self.question.id})"

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    option = models.ForeignKey(Option, on_delete=models.CASCADE, related_name='correct_for')

    class Meta:
        unique_together = ('question', 'option')

    def __str__(self):
        return f"Correct: {self.option.text[:50]} (Q: {self.question.id})"




class QuizAttempt(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='quiz_attempts')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    score = models.FloatField(default=0.0)
    is_submitted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('student', 'quiz')

    def __str__(self):
        return f"{self.student.user.full_name} → {self.quiz.title}"


class QuestionResponse(models.Model):
    attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name='responses')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='responses')
    selected_options = models.ManyToManyField(Option, related_name='selected_in_responses')  # allows multi-select
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.attempt.student.user.full_name} - Q{self.question.id}"
    
    
    
    