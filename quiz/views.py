from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from quiz.serializers import QuizCreateSerializer,QuizAttemptSerializer,QuizListSerializer,QuizDetailWithQuestionsSerializer
from v1.models import Topic
from users.models import CustomUser
from students.models import StudentProfile
from .models import Quiz




# {
#   "title": "Algebra Basics Quiz",
#   "description": "Covers equations and expressions",
#   "quiz_type": "teacher",
#   "questions": [
#     {
#       "text": "What is 2 + 2?",
#       "marks": 1,
#       "is_multiple_choice": false,
#       "options": [
#         {"text": "3"},
#         {"text": "4"},
#         {"text": "5"}
#       ],
#       "correct_option_indexes": [1]
#     },
#     {
#       "text": "Select even numbers.",
#       "marks": 2,
#       "is_multiple_choice": true,
#       "options": [
#         {"text": "1"},
#         {"text": "2"},
#         {"text": "4"}
#       ],
#       "correct_option_indexes": [1, 2]
#     }
#   ]
# }




@swagger_auto_schema(
    method='post',
    request_body=QuizCreateSerializer,
    responses={201: "Quiz created", 400: "Validation error"},
    manual_parameters=[
        openapi.Parameter('topic_id', openapi.IN_PATH, description="ID of the topic", type=openapi.TYPE_INTEGER),
        openapi.Parameter('teacher_id', openapi.IN_PATH, description="ID of the teacher (for teacher quiz)", type=openapi.TYPE_INTEGER, required=True)
    ]
)
@api_view(['POST'])
@permission_classes([AllowAny])
def create_quiz(request, topic_id, teacher_id=None):
    try:
        topic = Topic.objects.get(id=topic_id)
    except Topic.DoesNotExist:
        return Response({"error": "Topic not found."}, status=status.HTTP_404_NOT_FOUND)

    teacher = None
    if teacher_id:
        try:
            teacher = CustomUser.objects.get(id=teacher_id, role='teacher')
        except CustomUser.DoesNotExist:
            return Response({"error": "Teacher not found or invalid role."}, status=status.HTTP_404_NOT_FOUND)

    serializer = QuizCreateSerializer(data=request.data, context={'topic': topic, 'teacher': teacher})
    if serializer.is_valid():
        quiz = serializer.save()
        return Response({"message": "Quiz created", "quiz_id": quiz.id}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# {
#   "quiz_id": 4,
#   "answers": [
#     {
#       "question_id": 10,
#       "selected_option_ids": [21]
#     },
#     {
#       "question_id": 11,
#       "selected_option_ids": [24, 25]
#     }
#   ]
# }




@swagger_auto_schema(
    method='post',
    request_body=QuizAttemptSerializer,
    responses={201: "Attempt submitted", 400: "Validation error"},
    manual_parameters=[
        openapi.Parameter('student_id', openapi.IN_PATH, type=openapi.TYPE_INTEGER, description="ID of the student")
    ]
)
@api_view(['POST'])
@permission_classes([AllowAny])
def submit_quiz_attempt(request, student_id):
    try:
        student = StudentProfile.objects.select_related('user').get(id=student_id)
    except StudentProfile.DoesNotExist:
        return Response({"error": "Student not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = QuizAttemptSerializer(data=request.data, context={'student': student})
    if serializer.is_valid():
        attempt = serializer.save()
        return Response({
            "message": "Quiz submitted successfully.",
            "score": attempt.score,
            "quiz_id": attempt.quiz.id,
            "attempt_id": attempt.id
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)












@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter(
            'topic_id',
            openapi.IN_PATH,
            type=openapi.TYPE_INTEGER,
            description='ID of the topic to fetch quizzes for',
            required=True,
        )
    ],
    responses={200: QuizListSerializer(many=True)}
)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_quizzes_by_topic(request, topic_id):
    quizzes = Quiz.objects.filter(topic_id=topic_id, is_active=True)
    serializer = QuizListSerializer(quizzes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)






@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter(
            'teacher_id',
            openapi.IN_PATH,
            type=openapi.TYPE_INTEGER,
            description='ID of the teacher',
            required=True,
        ),
        openapi.Parameter(
            'topic_id',
            openapi.IN_PATH,
            type=openapi.TYPE_INTEGER,
            description='ID of the topic',
            required=True,
        ),
    ],
    responses={200: QuizListSerializer(many=True)}
)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_teacher_quizzes_by_topic(request, teacher_id, topic_id):
    quizzes = Quiz.objects.filter(
        quiz_type='teacher',
        teacher_id=teacher_id,
        topic_id=topic_id,
        is_active=True
    )
    serializer = QuizListSerializer(quizzes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)








@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter(
            'quiz_id',
            openapi.IN_PATH,
            type=openapi.TYPE_INTEGER,
            required=True,
            description="Quiz ID to fetch details and questions"
        )
    ],
    responses={200: QuizDetailWithQuestionsSerializer()}
)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_quiz_detail_with_questions(request, quiz_id):
    try:
        quiz = Quiz.objects.get(id=quiz_id, is_active=True)
    except Quiz.DoesNotExist:
        return Response({"error": "Quiz not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = QuizDetailWithQuestionsSerializer(quiz)
    return Response(serializer.data, status=status.HTTP_200_OK)









@swagger_auto_schema(
    method='get',
    operation_summary="Get quizzes for a student",
    operation_description="Fetches all quizzes assigned to the student based on their topic and teacher mappings.",
    responses={
        200: openapi.Response(
            description="List of quizzes",
            examples={
                "application/json": {
                    "student_id": 5,
                    "quizzes": [
                        {
                            "id": 1,
                            "title": "Algebra Basics",
                            "description": "Quiz on Algebra fundamentals",
                            "quiz_type": "topic",
                            "topic": 3,
                            "teacher": None,
                            "created_at": "2025-07-24T12:00:00Z",
                            "is_active": True
                        },
                        {
                            "id": 2,
                            "title": "Science MCQs",
                            "description": "Teacher-based quiz",
                            "quiz_type": "teacher",
                            "topic": 3,
                            "teacher": 9,
                            "created_at": "2025-07-22T08:30:00Z",
                            "is_active": True
                        }
                    ]
                }
            }
        ),
        404: "Student not found"
    }
)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_quizzes_for_student(request, student_id):
    try:
        student_profile = StudentProfile.objects.get(id=student_id)
        student_user = student_profile.user
    except StudentProfile.DoesNotExist:
        return Response({"error": "Student not found."}, status=status.HTTP_404_NOT_FOUND)

    # Get the class assigned to this student
    try:
        student_class = student_profile.class_assignment.class_model
    except:
        return Response({"error": "Student not assigned to a class."}, status=status.HTTP_404_NOT_FOUND)

    # Get quizzes where the topic's subject's class matches the student's class
    quizzes = Quiz.objects.filter(
        quiz_type='topic',
        topic__chapter__subject__class_model=student_class,
        is_active=True
    )

    # You can customize this as needed
    quiz_list = [
        {
            "id": quiz.id,
            "title": quiz.title,
            "description": quiz.description,
            "topic": quiz.topic.title,
            "subject": quiz.topic.chapter.subject.name,
            "chapter": quiz.topic.chapter.title,
            "quiz_type": quiz.get_quiz_type_display(),
            "created_at": quiz.created_at,
        }
        for quiz in quizzes
    ]

    return Response(quiz_list, status=status.HTTP_200_OK)







# ---------------- Get All Quizzes ----------------
@swagger_auto_schema(
    method='get',
    operation_summary="Get all quizzes",
    operation_description="Fetches all quizzes (active and inactive).",
    responses={200: QuizListSerializer(many=True)}
)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_quizzes(request):
    quizzes = Quiz.objects.all()
    serializer = QuizListSerializer(quizzes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# ---------------- Update Quiz ----------------
@swagger_auto_schema(
    method='put',
    operation_summary="Update a quiz",
    operation_description="Updates the quiz details (title, description, quiz_type).",
    request_body=QuizCreateSerializer,
    manual_parameters=[
        openapi.Parameter(
            'quiz_id',
            openapi.IN_PATH,
            type=openapi.TYPE_INTEGER,
            description="ID of the quiz to update",
            required=True
        ),
    ],
    responses={
        200: openapi.Response(
            description="Quiz updated successfully",
            examples={"application/json": {"message": "Quiz updated successfully.", "quiz_id": 3}}
        ),
        400: "Validation error",
        404: "Quiz not found"
    }
)
@api_view(['PUT'])
@permission_classes([AllowAny])
def update_quiz(request, quiz_id):
    try:
        quiz = Quiz.objects.get(id=quiz_id)
    except Quiz.DoesNotExist:
        return Response({"error": "Quiz not found."}, status=status.HTTP_404_NOT_FOUND)

    topic = quiz.topic
    teacher = quiz.teacher

    serializer = QuizCreateSerializer(
        quiz, data=request.data, context={'topic': topic, 'teacher': teacher}
    )

    if serializer.is_valid():
        validated_data = serializer.validated_data
        quiz.title = validated_data['title']
        quiz.description = validated_data.get('description', '')
        quiz.quiz_type = validated_data['quiz_type']
        quiz.save()

        return Response({"message": "Quiz updated successfully.", "quiz_id": quiz.id}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ---------------- Delete Quiz ----------------
@swagger_auto_schema(
    method='delete',
    operation_summary="Delete a quiz",
    operation_description="Deletes the quiz with the given ID.",
    manual_parameters=[
        openapi.Parameter(
            'quiz_id',
            openapi.IN_PATH,
            type=openapi.TYPE_INTEGER,
            description="ID of the quiz to delete",
            required=True
        ),
    ],
    responses={
        204: openapi.Response(
            description="Quiz deleted successfully",
            examples={"application/json": {"message": "Quiz deleted successfully."}}
        ),
        404: "Quiz not found"
    }
)
@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_quiz(request, quiz_id):
    try:
        quiz = Quiz.objects.get(id=quiz_id)
    except Quiz.DoesNotExist:
        return Response({"error": "Quiz not found."}, status=status.HTTP_404_NOT_FOUND)

    quiz.delete()
    return Response({"message": "Quiz deleted successfully."}, status=status.HTTP_204_NO_CONTENT)




