from rest_framework import serializers
from v1.models import (
    Content,
    Topic,
    Content,
    Subject
)
from teachers.models import TeacherNote

class ContentCompleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ['id', 'completed']




class ContentInputSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    video_link = serializers.URLField(required=False, allow_blank=True)
    text_content = serializers.CharField(required=False, allow_blank=True)
    order = serializers.IntegerField(default=1)
    is_active = serializers.BooleanField(default=True)

class TopicWithContentSerializer(serializers.Serializer):
    chapter_id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    number = serializers.IntegerField()
    description = serializers.CharField(required=False, allow_blank=True)
    contents = ContentInputSerializer(many=True)

    def create(self, validated_data):
        contents_data = validated_data.pop('contents')
        chapter_id = validated_data.pop('chapter_id')

        topic = Topic.objects.create(chapter_id=chapter_id, **validated_data)

        for content_data in contents_data:
            Content.objects.create(topic=topic, **content_data)

        return topic





class SubjectListSerializer(serializers.ModelSerializer):
    class_name = serializers.CharField(source='class_model.class_name')
    section = serializers.CharField(source='class_model.section')

    class Meta:
        model = Subject
        fields = ['id', 'name', 'code', 'description', 'class_name', 'section']





class ContentMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ['id', 'title', 'video_link', 'text_content', 'order', 'is_active', 'is_completed']

class TopicWithContentsSerializerV2(serializers.ModelSerializer):
    contents = ContentMiniSerializer(many=True)

    class Meta:
        model = Topic
        fields = ['id', 'title', 'number', 'description', 'is_completed', 'contents']





class TeacherNoteSerializerV1(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.user.full_name', read_only=True)

    class Meta:
        model = TeacherNote
        fields = ['id', 'teacher_name', 'note_text', 'note_file', 'created_at']




