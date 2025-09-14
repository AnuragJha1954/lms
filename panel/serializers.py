from rest_framework import serializers
from v1.models import Subject, Chapter, Topic, Content
from students.models import StudentProfile

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"


class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = "__all__"


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = "__all__"


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = "__all__"

class AssignStudentSerializer(serializers.Serializer):
    student_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False,
        help_text="List of Student IDs to assign"
    )

    def validate_student_ids(self, value):
        students = StudentProfile.objects.filter(id__in=value)
        if len(students) != len(set(value)):
            raise serializers.ValidationError("Some student IDs are invalid")
        return value

    def save(self, subject):
        student_ids = self.validated_data['student_ids']
        students = StudentProfile.objects.filter(id__in=student_ids)
        subject.students.add(*students)
        return subject
