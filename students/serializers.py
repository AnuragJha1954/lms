from rest_framework import serializers
from .models import (
    StudentProfile,
    TopicProgress,
    AssignedChapterTopic
)

from v1.models import (
    Subject,
    Chapter,
    Topic,
    Content
)

from teachers.models import (
    Teacher
)



class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = '__all__'  # or list specific fields if you prefer
        read_only_fields = ('student',)  # student FK should not be changed directly via API
        depth=1




class SubjectCompletionSerializer(serializers.Serializer):
    subject_name = serializers.CharField()
    completion_percentage = serializers.DecimalField(max_digits=5, decimal_places=2)




class IncompleteTopicSerializer(serializers.Serializer):
    topic_name = serializers.CharField()
    subject_name = serializers.CharField()
    chapter_name = serializers.CharField()
    completion_percentage = serializers.DecimalField(max_digits=5, decimal_places=2)
    last_accessed = serializers.DateTimeField()
    




class SubjectSerializer(serializers.ModelSerializer):
    assigned_teacher_name = serializers.CharField(source='assigned_teacher.user.full_name', read_only=True)
    class Meta:
        model = Subject
        fields = ['id', 'name', 'description', 'assigned_teacher_name']
        




class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ['id', 'content_link', 'description', 'completed']






class TopicWithProgressSerializer(serializers.ModelSerializer):
    contents = serializers.SerializerMethodField()
    completion_percentage = serializers.SerializerMethodField()
    last_accessed = serializers.SerializerMethodField()

    class Meta:
        model = Topic
        fields = ['id', 'name', 'description', 'contents', 'completion_percentage', 'last_accessed']

    def get_contents(self, topic):
        contents = Content.objects.filter(topic=topic)
        return ContentSerializer(contents, many=True).data

    def get_completion_percentage(self, topic):
        user = self.context.get('user')
        progress = TopicProgress.objects.filter(topic=topic, student=user).first()
        return progress.completion_percentage if progress else 0.0

    def get_last_accessed(self, topic):
        user = self.context.get('user')
        progress = TopicProgress.objects.filter(topic=topic, student=user).first()
        return progress.last_accessed if progress else None






class ChapterWithTopicsSerializer(serializers.ModelSerializer):
    topics = serializers.SerializerMethodField()

    class Meta:
        model = Chapter
        fields = ['id', 'name', 'description', 'topics']

    def get_topics(self, chapter):
        user = self.context.get('user')
        assigned = AssignedChapterTopic.objects.filter(student__user=user, chapter=chapter).first()
        if not assigned:
            return []
        topics = assigned.topics.all()
        return TopicWithProgressSerializer(topics, many=True, context={'user': user}).data


