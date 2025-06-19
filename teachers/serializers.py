from rest_framework import serializers
from users.models import CustomUser
from teachers.models import TeacherProfile, TeacherNote
from school.models import SchoolProfile
from students.models import StudentProfile
from v1.models import ClassModel

class TeacherCreateSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    username = serializers.CharField(write_only=True)
    assigned_class_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True
    )

    class Meta:
        model = TeacherProfile
        fields = [
            'full_name', 'username', 'email',
            'subject_specialization', 'phone_number', 'qualification',
            'date_of_birth', 'gender', 'address',
            'experience_years', 'profile_picture', 'assigned_class_ids'
        ]

    def create(self, validated_data):
        full_name = validated_data.pop('full_name')
        email = validated_data.pop('email')
        username = validated_data.pop('username')
        assigned_class_ids = validated_data.pop('assigned_class_ids')
        school = self.context['request'].user.school_profile

        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password='demo@123',
            full_name=full_name,
            role='teacher'
        )

        teacher = TeacherProfile.objects.create(user=user, school=school, **validated_data)
        teacher.assigned_classes.set(ClassModel.objects.filter(id__in=assigned_class_ids))
        return teacher







class StudentListSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='user.full_name')
    email = serializers.EmailField(source='user.email')
    class_name = serializers.CharField(source='class_assignment.class_model.class_name', read_only=True)
    section = serializers.CharField(source='class_assignment.class_model.section', read_only=True)

    class Meta:
        model = StudentProfile
        fields = [
            'id', 'full_name', 'email', 'roll_number',
            'guardian_name', 'contact_number',
            'class_name', 'section'
        ]






class TeacherNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherNote
        fields = ['id', 'topic', 'note_text', 'note_file', 'created_at']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        teacher = self.context['request'].user.teacher_profile
        return TeacherNote.objects.create(teacher=teacher, **validated_data)
