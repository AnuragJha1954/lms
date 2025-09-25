from rest_framework import serializers
from users.models import CustomUser
from students.models import StudentProfile, StudentClassAssignment, TopicProgress, ContentProgress, TopicAccessLog, StudentLoginActivity
from v1.models import ClassModel,Chapter,Subject,Topic,Content
from school.models import SchoolProfile

class StudentCreateSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)


    class Meta:
        model = StudentProfile
        fields = [
            'full_name',  'email', 'roll_number', 'guardian_name',
            'contact_number', 'date_of_birth', 'gender', 'address',
            'admission_date', 'profile_picture'
        ]

    def create(self, validated_data):
        full_name = validated_data.pop('full_name')
        email = validated_data.pop('email')
        school = self.context['school']

        user = CustomUser.objects.create_user(
            email=email,
            password='demo@123',
            full_name=full_name,
            role='student'
        )

        student = StudentProfile.objects.create(user=user, school=school, **validated_data)
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



class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ["id", "title", "number", "description"]  # match model fields

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ["id", "title", "number", "description", "is_completed"]

class GetContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ["id", "title", "video_link", "text_content", "order", "is_active", "is_completed"]

class TopicWithContentSerializer(serializers.ModelSerializer):
    contents = GetContentSerializer(many=True, read_only=True)

    class Meta:
        model = Topic
        fields = ["id", "title", "number", "description", "is_completed", "contents"]
        ref_name = "StudentTopicWithContent"  # <-- unique name for Swagger