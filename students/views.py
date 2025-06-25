from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import StudentCreateSerializer, ContentProgressSerializer, TopicProgressSerializer, LastAccessedTopicSerializer, StudentLastLoginSerializer, StudentProfileSerializer
from students.models import ContentProgress, TopicProgress, TopicAccessLog, StudentLoginActivity, StudentProfile
from v1.models import Content, Topic
from users.models import CustomUser





@swagger_auto_schema(
    method='post',
    request_body=StudentCreateSerializer,
    responses={201: "Student created", 400: "Validation error"}
)
@api_view(['POST'])
@permission_classes([AllowAny])
def create_student(request, school_user_id):
    try:
        school_user = CustomUser.objects.get(id=school_user_id, role='school')
        school = school_user.school_profile
    except CustomUser.DoesNotExist:
        return Response({"error": "School user not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return Response({"error": "School profile not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = StudentCreateSerializer(data=request.data, context={'school': school})
    if serializer.is_valid():
        student = serializer.save()
        return Response(StudentCreateSerializer(student).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






@swagger_auto_schema(
    method='post',
    request_body=ContentProgressSerializer,
    responses={200: "Content progress updated"}
)
@api_view(['POST'])
@permission_classes([AllowAny])
def mark_content_progress(request):
    serializer = ContentProgressSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data
        student = request.user.student_profile
        content = Content.objects.get(id=data['content_id'])

        progress, _ = ContentProgress.objects.get_or_create(
            student=student, content=content
        )
        progress.is_completed = data['is_completed']
        if data['is_completed']:
            from django.utils import timezone
            progress.completed_at = timezone.now()
        progress.save()
        return Response({"message": "Content progress updated."})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





@swagger_auto_schema(
    method='post',
    request_body=TopicProgressSerializer,
    responses={200: "Topic progress updated"}
)
@api_view(['POST'])
@permission_classes([AllowAny])
def mark_topic_progress(request):
    serializer = TopicProgressSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data
        student = request.user.student_profile
        topic = Topic.objects.get(id=data['topic_id'])

        progress, _ = TopicProgress.objects.get_or_create(
            student=student, topic=topic
        )
        progress.completion_percentage = data['completion_percentage']
        progress.is_completed = data['is_completed']
        progress.save()

        # Log last accessed
        TopicAccessLog.objects.create(student=student, topic=topic)

        return Response({"message": "Topic progress updated."})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







@swagger_auto_schema(
    method='get',
    responses={200: LastAccessedTopicSerializer(many=True)}
)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_last_accessed_topics(request):
    student = request.user.student_profile

    topic_progress_qs = TopicProgress.objects.filter(
        student=student,
        completion_percentage__lt=100.0
    ).select_related(
        'topic__chapter__subject'
    ).order_by('-last_accessed', '-completion_percentage')[:5]

    serializer = LastAccessedTopicSerializer(topic_progress_qs, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)






@swagger_auto_schema(
    method='post',
    responses={200: "Login time recorded successfully"}
)
@api_view(['POST'])
@permission_classes([AllowAny])
def store_student_login(request, student_id):
    try:
        student = StudentProfile.objects.get(id=student_id)
    except StudentProfile.DoesNotExist:
        return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

    StudentLoginActivity.objects.create(student=student)
    return Response({"message": "Login time recorded successfully"}, status=status.HTTP_200_OK)









@swagger_auto_schema(
    method='get',
    responses={200: StudentLastLoginSerializer}
)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_last_login_info(request, student_id):
    try:
        student = StudentProfile.objects.get(id=student_id)
    except StudentProfile.DoesNotExist:
        return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

    last_login = StudentLoginActivity.objects.filter(student=student).order_by('-login_time').first()
    if last_login:
        serializer = StudentLastLoginSerializer(last_login)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"message": "No login record found."}, status=status.HTTP_404_NOT_FOUND)







@swagger_auto_schema(
    method='get',
    responses={200: StudentProfileSerializer}
)
@swagger_auto_schema(
    method='put',
    request_body=StudentProfileSerializer,
    responses={200: StudentProfileSerializer}
)
@api_view(['GET', 'PUT'])
@permission_classes([AllowAny])
def manage_student_profile(request, student_id):
    try:
        student_profile = StudentProfile.objects.get(id=student_id)
    except StudentProfile.DoesNotExist:
        return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = StudentProfileSerializer(student_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = StudentProfileSerializer(student_profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)