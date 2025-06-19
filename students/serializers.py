from rest_framework import serializers
from users.models import CustomUser
from students.models import StudentProfile, StudentClassAssignment, TopicProgress, ContentProgress, TopicAccessLog, StudentLoginActivity
from v1.models import ClassModel
from school.models import SchoolProfile

class StudentCreateSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    username = serializers.CharField(write_only=True)
    class_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = StudentProfile
        fields = [
            'full_name', 'username', 'email', 'roll_number', 'guardian_name',
            'contact_number', 'date_of_birth', 'gender', 'address',
            'admission_date', 'profile_picture', 'class_id'
        ]

    def create(self, validated_data):
        full_name = validated_data.pop('full_name')
        email = validated_data.pop('email')
        username = validated_data.pop('username')
        class_id = validated_data.pop('class_id')
        school = self.context['request'].user.school_profile

        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password='demo@123',
            full_name=full_name,
            role='student'
        )

        student = StudentProfile.objects.create(user=user, school=school, **validated_data)
        StudentClassAssignment.objects.create(student=student, class_model_id=class_id)
        return student





class ContentProgressSerializer(serializers.Serializer):
    content_id = serializers.IntegerField()
    is_completed = serializers.BooleanField()

class TopicProgressSerializer(serializers.Serializer):
    topic_id = serializers.IntegerField()
    completion_percentage = serializers.FloatField(min_value=0.0, max_value=100.0)
    is_completed = serializers.BooleanField()

class TopicAccessLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicAccessLog
        fields = ['id', 'topic', 'accessed_at']





class LastAccessedTopicSerializer(serializers.ModelSerializer):
    topic_title = serializers.CharField(source='topic.title')
    chapter_title = serializers.CharField(source='topic.chapter.title')
    subject_name = serializers.CharField(source='topic.chapter.subject.name')
    last_accessed = serializers.DateTimeField()
    completion_percentage = serializers.FloatField()

    class Meta:
        model = TopicProgress
        fields = ['topic_title', 'chapter_title', 'subject_name', 'completion_percentage', 'last_accessed']






class StudentLastLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentLoginActivity
        fields = ['login_time']




class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = '__all__'



