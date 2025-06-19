from rest_framework.decorators import api_view, permission_classes,parser_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import TeacherCreateSerializer, StudentListSerializer, TeacherNoteSerializer
from v1.models import TeacherSubjectAssignment,Content, Topic
from students.models import StudentClassAssignment







@swagger_auto_schema(
    method='post',
    request_body=TeacherCreateSerializer,
    responses={201: "Teacher created", 400: "Validation error"}
)
@api_view(['POST'])
@permission_classes([AllowAny])
def create_teacher(request):
    serializer = TeacherCreateSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        teacher = serializer.save()
        return Response(TeacherCreateSerializer(teacher).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
















@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter(
            'subject_id',
            openapi.IN_QUERY,
            type=openapi.TYPE_INTEGER,
            required=False,
            description="Filter students by subject ID"
        )
    ],
    responses={200: StudentListSerializer(many=True)}
)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_teacher_students(request):
    teacher = request.user.teacher_profile
    subject_id = request.GET.get('subject_id')

    class_ids = teacher.assigned_classes.values_list('id', flat=True)

    if subject_id:
        try:
            subject_class = TeacherSubjectAssignment.objects.get(
                teacher=teacher, subject_id=subject_id
            ).subject.class_model_id
        except TeacherSubjectAssignment.DoesNotExist:
            return Response({"error": "Subject not found or not assigned."}, status=404)
        class_ids = [subject_class]

    students = StudentClassAssignment.objects.filter(class_model_id__in=class_ids).select_related('student__user', 'class_model')
    student_profiles = [s.student for s in students]

    serializer = StudentListSerializer(student_profiles, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)











@swagger_auto_schema(
    method='post',
    request_body=TeacherNoteSerializer,
    responses={201: "Note added successfully", 400: "Validation Error"}
)
@api_view(['POST'])
@permission_classes([AllowAny])
@parser_classes([MultiPartParser, FormParser])
def add_teacher_note(request):
    serializer = TeacherNoteSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        note = serializer.save()
        return Response(TeacherNoteSerializer(note).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)












@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['content_id'],
        properties={
            'content_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the content to mark as completed')
        },
    ),
    responses={200: "Content marked as completed", 404: "Content not found"}
)
@api_view(['POST'])
@permission_classes([AllowAny])
def mark_content_completed(request):
    content_id = request.data.get('content_id')
    if not content_id:
        return Response({"error": "content_id is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        content = Content.objects.get(id=content_id)
    except Content.DoesNotExist:
        return Response({"error": "Content not found"}, status=status.HTTP_404_NOT_FOUND)

    content.is_completed = True
    content.save()
    return Response({"message": f"Content '{content.title}' marked as completed."}, status=status.HTTP_200_OK)








@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['topic_id'],
        properties={
            'topic_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the topic to mark as completed')
        },
    ),
    responses={200: "Topic marked as completed", 404: "Topic not found"}
)
@api_view(['POST'])
@permission_classes([AllowAny])
def mark_topic_completed(request):
    topic_id = request.data.get('topic_id')
    if not topic_id:
        return Response({"error": "topic_id is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        topic = Topic.objects.get(id=topic_id)
    except Topic.DoesNotExist:
        return Response({"error": "Topic not found"}, status=status.HTTP_404_NOT_FOUND)

    topic.is_completed = True
    topic.save()
    return Response({"message": f"Topic '{topic.title}' marked as completed."}, status=status.HTTP_200_OK)



