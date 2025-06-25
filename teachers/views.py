from rest_framework.decorators import api_view, permission_classes,parser_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import TeacherCreateSerializer, StudentListSerializer, TeacherNoteSerializer, TeacherListSerializer
from v1.models import TeacherSubjectAssignment,Content, Topic
from students.models import StudentClassAssignment
from users.models import CustomUser
from school.models import SchoolProfile 
from .models import TeacherProfile





@swagger_auto_schema(
    method='post',
    request_body=TeacherCreateSerializer,
    responses={201: "Teacher created", 400: "Validation error"},
    manual_parameters=[
        openapi.Parameter(
            'school_user_id',
            openapi.IN_PATH,
            type=openapi.TYPE_INTEGER,
            required=True,
            description='User ID of the school owner'
        )
    ]
)
@api_view(['POST'])
@permission_classes([AllowAny])
def create_teacher(request, school_user_id):
    try:
        school_user = CustomUser.objects.get(id=school_user_id, role='school')
        school = school_user.school_profile
    except CustomUser.DoesNotExist:
        return Response({"error": "School user not found."}, status=status.HTTP_404_NOT_FOUND)
    except SchoolProfile.DoesNotExist:
        return Response({"error": "School profile not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = TeacherCreateSerializer(data=request.data, context={'school': school})
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
def get_teacher_students(request, teacher_user_id):
    try:
        teacher_user = CustomUser.objects.get(id=teacher_user_id, role='teacher')
        teacher = teacher_user.teacher_profile
    except CustomUser.DoesNotExist:
        return Response({"error": "Teacher user not found."}, status=404)
    except TeacherProfile.DoesNotExist:
        return Response({"error": "Teacher profile not found."}, status=404)

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

    students = StudentClassAssignment.objects.filter(
        class_model_id__in=class_ids
    ).select_related('student__user', 'class_model')

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
def add_teacher_note(request, teacher_user_id):
    try:
        teacher = TeacherProfile.objects.get(user_id=teacher_user_id)
    except TeacherProfile.DoesNotExist:
        return Response({"error": "Teacher profile not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = TeacherNoteSerializer(data=request.data, context={'teacher': teacher})
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









@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter(
            'user_id',
            openapi.IN_PATH,
            description="User ID of the school",
            type=openapi.TYPE_INTEGER,
            required=True
        )
    ],
    responses={200: TeacherListSerializer(many=True), 404: 'School not found'}
)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_teachers_by_school(request, school_user_id):
    try:
        school_user = CustomUser.objects.get(id=school_user_id, role='school')
        school_profile = school_user.school_profile
    except CustomUser.DoesNotExist:
        return Response({"error": "School user not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return Response({"error": "School profile not found."}, status=status.HTTP_404_NOT_FOUND)

    teachers = TeacherProfile.objects.filter(school=school_profile).select_related('user')
    serializer = TeacherListSerializer(teachers, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)




