from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from .serializers import TopicWithContentSerializer, SubjectListSerializer, TopicWithContentsSerializerV2, TeacherNoteSerializerV1
from drf_yasg import openapi
from v1.models import Subject, Chapter, Topic
from teachers.models import TeacherNote






# {
#   "chapter_id": 5,
#   "title": "Photosynthesis",
#   "number": 3,
#   "description": "This topic explains the process of photosynthesis.",
#   "contents": [
#     {
#       "title": "Introduction Video",
#       "video_link": "https://youtube.com/abc123",
#       "text_content": "Watch this video to understand the basics.",
#       "order": 1,
#       "is_active": true
#     },
#     {
#       "title": "Text Notes",
#       "text_content": "Photosynthesis is a process by which plants prepare food...",
#       "order": 2
#     }
#   ]
# }






@swagger_auto_schema(
    method='post',
    request_body=TopicWithContentSerializer,
    responses={201: "Topic and content created", 400: "Bad Request"}
)
@api_view(['POST'])
@permission_classes([AllowAny])
def add_topic_with_content(request):
    serializer = TopicWithContentSerializer(data=request.data)
    if serializer.is_valid():
        topic = serializer.save()
        return Response({
            "message": "Topic and contents added successfully.",
            "topic_id": topic.id,
            "topic_title": topic.title
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)








@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter(
            'class_id',
            openapi.IN_QUERY,
            type=openapi.TYPE_INTEGER,
            required=True,
            description='ID of the class to fetch subjects for'
        )
    ],
    responses={200: SubjectListSerializer(many=True)}
)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_subjects_by_class(request):
    class_id = request.GET.get('class_id')
    if not class_id:
        return Response({"error": "class_id is required"}, status=status.HTTP_400_BAD_REQUEST)

    subjects = Subject.objects.filter(class_model_id=class_id)
    serializer = SubjectListSerializer(subjects, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)









@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter(
            'subject_id',
            openapi.IN_QUERY,
            type=openapi.TYPE_INTEGER,
            required=True,
            description='ID of the subject to fetch topics and contents for'
        )
    ],
    responses={200: TopicWithContentsSerializerV2(many=True)}
)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_topics_with_contents_by_subject(request):
    subject_id = request.GET.get('subject_id')
    if not subject_id:
        return Response({"error": "subject_id is required"}, status=status.HTTP_400_BAD_REQUEST)

    topic_qs = Topic.objects.filter(chapter__subject_id=subject_id).prefetch_related('contents')
    serializer = TopicWithContentsSerializerV2(topic_qs, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)





@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter(
            'topic_id',
            openapi.IN_QUERY,
            type=openapi.TYPE_INTEGER,
            required=True,
            description='ID of the topic to fetch teacher notes for'
        )
    ],
    responses={200: TeacherNoteSerializerV1(many=True)}
)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_teacher_notes_by_topic(request):
    topic_id = request.GET.get('topic_id')
    if not topic_id:
        return Response({"error": "topic_id is required"}, status=status.HTTP_400_BAD_REQUEST)

    notes = TeacherNote.objects.filter(topic_id=topic_id)
    serializer = TeacherNoteSerializerV1(notes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


