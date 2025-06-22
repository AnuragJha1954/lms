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









