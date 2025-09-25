from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, AllowAny
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import ChapterSerializer, StudentCreateSerializer, ContentProgressSerializer, TopicProgressSerializer, LastAccessedTopicSerializer, StudentLastLoginSerializer, StudentProfileSerializer, TopicSerializer, TopicWithContentSerializer, GetContentSerializer
from students.models import ContentProgress, TopicProgress, TopicAccessLog, StudentLoginActivity, StudentProfile, StudentClassAssignment
from v1.models import Content, Topic, Subject, Chapter, ClassModel
from users.models import CustomUser
from datetime import timedelta




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
def get_last_accessed_topics(request, student_id):
    try:
        student = StudentProfile.objects.get(user_id=student_id)
    except StudentProfile.DoesNotExist:
        return Response({"error": "Student profile not found"}, status=status.HTTP_404_NOT_FOUND)

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
    responses={
        200: openapi.Response(
            description="Student profile retrieved successfully.",
            examples={
                "application/json": {
                    "id": 1,
                    "user": 5,
                    "school": 2,
                    "roll_number": "STU123",
                    "guardian_name": "Ravi Kumar",
                    "contact_number": "9876543210",
                    "date_of_birth": "2008-05-15",
                    "gender": "Male",
                    "address": "123 Green Avenue, Delhi",
                    "full_name": "Amit Sharma",
                    "gpa": 8.5,
                    "class": "10-A"
                }
            }
        ),
        404: "Student not found"
    }
)
@swagger_auto_schema(
    method='put',
    request_body=StudentProfileSerializer,
    responses={
        200: openapi.Response(
            description="Student profile updated successfully.",
            examples={
                "application/json": {
                    "id": 1,
                    "user": 5,
                    "school": 2,
                    "roll_number": "STU123",
                    "guardian_name": "Ravi Kumar",
                    "contact_number": "9876543210",
                    "date_of_birth": "2008-05-15",
                    "gender": "Male",
                    "address": "123 Green Avenue, Delhi",
                    "full_name": "Amit Sharma",
                    "gpa": 8.5,
                    "class": "10-A"
                }
            }
        ),
        400: "Validation Error"
    }
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
        data = serializer.data

        # Add user full name
        data['full_name'] = student_profile.user.full_name

        # Add hardcoded GPA
        data['gpa'] = 8.5

        # Add class name
        try:
            assignment = StudentClassAssignment.objects.get(student=student_profile)
            data['class'] = assignment.class_model.class_name  # Adjust if your field name is different
        except StudentClassAssignment.DoesNotExist:
            data['class'] = None

        return Response(data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = StudentProfileSerializer(student_profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            # Re-fetch for updated data
            updated_data = serializer.data
            updated_data['full_name'] = student_profile.user.full_name
            updated_data['gpa'] = 8.5
            try:
                assignment = StudentClassAssignment.objects.get(student=student_profile)
                updated_data['class'] = assignment.class_model.class_name
            except StudentClassAssignment.DoesNotExist:
                updated_data['class'] = None

            return Response(updated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    





# 1. Get Subjects for Student
@api_view(["GET"])
@permission_classes([AllowAny])
def get_my_subjects(request):
    try:
        class_assignment = StudentClassAssignment.objects.get(student__user=request.user)
    except StudentClassAssignment.DoesNotExist:
        return Response({"error": "Student not assigned to any class"}, status=404)

    subjects = Subject.objects.filter(class_model=class_assignment.class_model)
    data = [
        {"id": s.id, "name": s.name, "code": s.code, "description": s.description}
        for s in subjects
    ]
    return Response(data)


# 2. Get All Chapters for a Subject
@api_view(["GET"])
@permission_classes([AllowAny])
def get_subject_chapters(request, subject_id):
    chapters = Chapter.objects.filter(subject_id=subject_id).order_by("number")
    data = [
        {"id": c.id, "title": c.title, "number": c.number, "description": c.description}
        for c in chapters
    ]
    return Response(data)


# 3. Get Topics + Contents for a Chapter
@api_view(["GET"])
@permission_classes([AllowAny])
def get_chapter_topics(request, chapter_id):
    topics = Topic.objects.filter(chapter_id=chapter_id).order_by("number")
    data = []
    for t in topics:
        contents = Content.objects.filter(topic=t, is_active=True).order_by("order")
        data.append({
            "id": t.id,
            "title": t.title,
            "number": t.number,
            "description": t.description,
            "is_completed": t.is_completed,
            "contents": [
                {
                    "id": c.id,
                    "title": c.title,
                    "video_link": c.video_link,
                    "text_content": c.text_content,
                    "order": c.order,
                    "is_active": c.is_active,
                    "is_completed": c.is_completed,
                }
                for c in contents
            ]
        })
    return Response(data)


@swagger_auto_schema(
    method='get',
    operation_summary="Get Student Dashboard",
    operation_description="""
    Returns student dashboard data including:
    1. Four recently accessed topics with completion %
    2. List of all subjects with completion %
    3. Current learning streak (consecutive days logged in)
    4. Hardcoded 3 reports
    5. Hardcoded list of badges
    """,
    responses={200: openapi.Response(
        description="Dashboard data",
        examples={
            "application/json": {
                "recent_topics": [
                    {"topic": "Algebra Basics", "chapter": "Mathematics", "completion_percentage": 50.0, "last_accessed": "2025-09-13T10:00:00Z"}
                ],
                "subjects": [
                    {"subject": "Mathematics", "completion_percentage": 70.5}
                ],
                "learning_streak": 5,
                "reports": ["Performance Report", "Attendance Report", "Progress Report"],
                "badges": ["Concept Conqueror", "Chapter Champion", "Subject Specialist"]
            }
        }
    )}
)
@api_view(["GET"])
@permission_classes([AllowAny])
def student_dashboard(request, user_id):
    try:
        student = StudentProfile.objects.get(user_id=user_id)
    except StudentProfile.DoesNotExist:
        return Response({"error": "Student profile not found"}, status=404)

    # 1. Recently accessed topics (limit 4)
    recent_topics_qs = TopicProgress.objects.filter(student=student).order_by("-last_accessed")[:4]
    recent_topics = [
        {
            "topic": tp.topic.title,
            "chapter": tp.topic.chapter.title,
            "completion_percentage": tp.completion_percentage,
            "last_accessed": tp.last_accessed,
        }
        for tp in recent_topics_qs
    ]

    # 2. Subjects with completion %
    # 2. Subjects with completion %
    subjects_qs = student.subjects.all()  # Related name on Subject: 'subjects'
    subjects = []

    for subj in subjects_qs:
        # Total number of topics under this subject
        total_topics = Topic.objects.filter(chapter__subject=subj).count()

        # Number of topics the student has completed
        completed_topics = TopicProgress.objects.filter(
            student=student,
            topic__chapter__subject=subj,
            is_completed=True
        ).count()

        # Completion percentage
        completion_percentage = (completed_topics / total_topics * 100) if total_topics > 0 else 0

        subjects.append({
            "subject": subj.name,
            "completion_percentage": round(completion_percentage, 2),
        })


    # 3. Learning streak
    streak = 0
    login_dates = StudentLoginActivity.objects.filter(student=student).order_by("-login_time").values_list("login_time", flat=True)

    if login_dates:
        streak = 1
        prev_date = login_dates[0].date()
        for login in login_dates[1:]:
            login_date = login.date()
            if prev_date - login_date == timedelta(days=1):
                streak += 1
                prev_date = login_date
            elif prev_date == login_date:
                continue
            else:
                break

    # 4. Hardcoded reports
    reports = ["Performance Report", "Attendance Report", "Progress Report"]

    # 5. Hardcoded badges
    badges = [
        "Concept Conqueror",
        "Chapter Champion",
        "Subject Specialist",
        "Streak Master",
        "Time Traveller",
        "Quiz Warrior",
        "First Step",
        "Halfway Hero",
        "Final Frontier",
        "Comeback Kid",
    ]

    return Response({
        "recent_topics": recent_topics,
        "subjects": subjects,
        "learning_streak": streak,
        "reports": reports,
        "badges": badges,
    })

    
    



# 1. Get all chapters of a subject
@swagger_auto_schema(
    method="get",
    responses={200: ChapterSerializer(many=True)},
    operation_description="Get all chapters of a subject"
)
@api_view(["GET"])
@permission_classes([])
def get_chapters_of_subject(request, subject_id):
    try:
        chapters = Chapter.objects.filter(subject_id=subject_id)
    except Subject.DoesNotExist:
        return Response({"error": "Subject not found"}, status=status.HTTP_404_NOT_FOUND)
    serializer = ChapterSerializer(chapters, many=True)
    return Response(serializer.data)


# 2. Get all topics in a chapter
@swagger_auto_schema(
    method="get",
    responses={200: TopicSerializer(many=True)},
    operation_description="Get all topics in a chapter"
)
@api_view(["GET"])
@permission_classes([])
def get_topics_of_chapter(request, chapter_id):
    try:
        topics = Topic.objects.filter(chapter_id=chapter_id)
    except Chapter.DoesNotExist:
        return Response({"error": "Chapter not found"}, status=status.HTTP_404_NOT_FOUND)
    serializer = TopicSerializer(topics, many=True)
    return Response(serializer.data)


# 3. Get all content of a topic
@swagger_auto_schema(
    method="get",
    responses={200: GetContentSerializer(many=True)},
    operation_description="Get all content of a topic"
)
@api_view(["GET"])
@permission_classes([])
def get_content_of_topic(request, topic_id):
    try:
        contents = Content.objects.filter(topic_id=topic_id)
    except Topic.DoesNotExist:
        return Response({"error": "Topic not found"}, status=status.HTTP_404_NOT_FOUND)
    serializer = GetContentSerializer(contents, many=True)
    return Response(serializer.data)


# 4. Get all topics with content for a chapter
@swagger_auto_schema(
    method="get",
    responses={200: TopicWithContentSerializer(many=True)},
    operation_description="Get all topics with their content for a chapter"
)
@api_view(["GET"])
@permission_classes([])
def get_topics_with_content_for_chapter(request, chapter_id):
    try:
        topics = Topic.objects.filter(chapter_id=chapter_id)
    except Chapter.DoesNotExist:
        return Response({"error": "Chapter not found"}, status=status.HTTP_404_NOT_FOUND)
    serializer = TopicWithContentSerializer(topics, many=True)
    return Response(serializer.data)