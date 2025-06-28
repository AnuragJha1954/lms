from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import LoginSerializer
from users.models import CustomUser
from school.models import SchoolProfile
from students.models import StudentProfile
from teachers.models import TeacherProfile


@swagger_auto_schema(
    method='post',
    operation_summary="User Login",
    operation_description="Authenticate user and return token and profile.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['email', 'password', 'role'],
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, format='email'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, format='password'),
            'role': openapi.Schema(type=openapi.TYPE_STRING),
        }
    ),
    responses={200: "Login successful", 400: "Invalid credentials"}
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)

        profile_data = None

        if user.role == 'school' and hasattr(user, 'school_profile'):
            profile = user.school_profile
            profile_data = {
                "id": profile.id,
                "name": profile.name,
                "phone_number": profile.phone_number,
                "registration_number": profile.registration_number,
                "address": profile.address,
                "board_affiliation": profile.board_affiliation,
                "principal_name": profile.principal_name,
                "established_year": profile.established_year,
                "website": profile.website,
                "logo": profile.logo.url if profile.logo else None
            }

        elif user.role == 'teacher' and hasattr(user, 'teacher_profile'):
            profile = user.teacher_profile
            profile_data = {
                "id": profile.id,
                "school_id": profile.school.id,
                "subject_specialization": profile.subject_specialization,
                "phone_number": profile.phone_number,
                "qualification": profile.qualification,
                "date_of_birth": profile.date_of_birth,
                "gender": profile.gender,
                "address": profile.address,
                "experience_years": profile.experience_years,
                "profile_picture": profile.profile_picture.url if profile.profile_picture else None
            }

        elif user.role == 'student' and hasattr(user, 'student_profile'):
            profile = user.student_profile
            profile_data = {
                "id": profile.id,
                "school_id": profile.school.id,
                "roll_number": profile.roll_number,
                "guardian_name": profile.guardian_name,
                "contact_number": profile.contact_number,
                "date_of_birth": profile.date_of_birth,
                "gender": profile.gender,
                "address": profile.address,
                "admission_date": profile.admission_date,
                "profile_picture": profile.profile_picture.url if profile.profile_picture else None
            }

        return Response({
            "token": token.key,
            "user": {
                "id": user.id,
                "email": user.email,
                "role": user.role,
                "name": user.full_name,  # ✅ Fixed line
                "profile": profile_data
            }
        }, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)









@swagger_auto_schema(
    method='post',
    operation_summary="User Logout",
    operation_description="Invalidate the current token.",
    manual_parameters=[
        openapi.Parameter(
            'Authorization',
            openapi.IN_HEADER,
            description='Authorization header: "Authorization: Token <your_token>"',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    responses={200: "Logged out successfully", 401: "Unauthorized"},
)
@api_view(['POST'])
@permission_classes([AllowAny])
def logout_view(request):
    if request.auth:
        request.auth.delete()
    return Response({"detail": "Logged out successfully"}, status=200)






@swagger_auto_schema(
    method='post',
    operation_summary="Refresh Token",
    operation_description="Refresh the user's auth token.",
    manual_parameters=[
        openapi.Parameter(
            'Authorization',
            openapi.IN_HEADER,
            description='Authorization header: "Authorization: Token <your_token>"',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    responses={200: "New token issued", 401: "Unauthorized"},
)
@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token_view(request):
    user = request.user
    if not user or not request.auth:
        return Response({"error": "Unauthorized"}, status=401)

    request.auth.delete()  # delete old token
    token = Token.objects.create(user=user)
    return Response({"token": token.key}, status=200)


