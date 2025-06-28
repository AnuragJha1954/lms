from rest_framework import serializers
from users.models import CustomUser
from v1.models import ClassModel, Subject, TeacherSubjectAssignment
from students.models import StudentProfile, StudentClassAssignment
from school.models import SchoolProfile

class SchoolRegistrationSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)

    class Meta:
        model = SchoolProfile
        fields = [
            'full_name', 'email',
            'name', 'address', 'phone_number',
            'registration_number', 'board_affiliation',
            'principal_name', 'established_year',
            'website', 'logo'
        ]

    def create(self, validated_data):
        full_name = validated_data.pop('full_name')
        email = validated_data.pop('email')

        user = CustomUser.objects.create_user(
            email=email,
            password='demo@123',
            full_name=full_name,
            role='school'
        )

        school_profile = SchoolProfile.objects.create(user=user, **validated_data)
        return school_profile






class SubjectInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    code = serializers.CharField(max_length=20, required=False, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True)


class ClassWithSubjectsSerializer(serializers.Serializer):
    class_name = serializers.CharField(max_length=20)
    section = serializers.CharField(max_length=10)
    academic_year = serializers.CharField(max_length=20, required=False, allow_blank=True)
    subjects = SubjectInputSerializer(many=True)

    def create(self, validated_data):
        subjects_data = validated_data.pop('subjects')
        school = self.context.get('school')
        class_model = ClassModel.objects.create(school=school, **validated_data)
        for subject in subjects_data:
            Subject.objects.create(class_model=class_model, **subject)
        return class_model








class TeacherSubjectAssignSerializer(serializers.Serializer):
    teacher_id = serializers.IntegerField()
    subject_id = serializers.IntegerField()

    def create(self, validated_data):
        return TeacherSubjectAssignment.objects.create(**validated_data)





class AssignStudentToClassSerializer(serializers.Serializer):
    student_id = serializers.IntegerField()
    class_id = serializers.IntegerField()

    def validate(self, data):
        # Optional: Add extra validation (e.g. prevent reassigning to same class)
        return data

    def create(self, validated_data):
        student = StudentProfile.objects.get(id=validated_data['student_id'])
        class_model = ClassModel.objects.get(id=validated_data['class_id'])

        # If already exists, update instead of error
        obj, created = StudentClassAssignment.objects.update_or_create(
            student=student,
            defaults={'class_model': class_model}
        )
        return obj



class SchoolProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolProfile
        fields = [
            'id', 'name', 'address', 'phone_number', 'registration_number',
            'board_affiliation', 'principal_name', 'established_year',
            'website', 'logo'
        ]
        read_only_fields = ['id', 'registration_number']  # prevent editing this if needed
