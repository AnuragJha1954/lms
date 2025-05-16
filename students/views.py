from django.shortcuts import render
from django.utils import timezone

from datetime import timedelta

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from v1.utils import get_user_from_token

from .models import (
    StudentProfile, 
    StudentSchool,
    TopicProgress
)

from users.models import CustomUser

from v1.models import (
    Subject, 
    Chapter, 
    Topic
)

from .serializers import (
    StudentProfileSerializer,
    SubjectCompletionSerializer, 
    IncompleteTopicSerializer, 
    SubjectSerializer, 
    ChapterWithTopicsSerializer,
    SubjectDashboardResponseSerializer
)


@swagger_auto_schema(
    method='get',
    operation_summary="Get Student Profile",
    operation_description="Retrieve the student profile by user ID. Only the user themselves can access.",
    responses={
        200: openapi.Response('Student profile retrieved', StudentProfileSerializer()),
        403: 'Permission denied',
        404: 'Student profile not found',
    },
    manual_parameters=[
        openapi.Parameter(
            'Authorization',
            openapi.IN_HEADER,
            description='Authorization token',
            type=openapi.TYPE_STRING,
            required=True
        ),
        openapi.Parameter(
            'user_id',
            openapi.IN_PATH,
            description='ID of the user to retrieve profile for',
            type=openapi.TYPE_STRING,
            required=True
        ),
    ]
)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_student_profile(request, user_id):
    user, error_response = get_user_from_token(request)
    if error_response:
        return error_response
    
    # Optionally, check if user_id matches token user or if user has permission
    if str(user.id) != str(user_id):
        return Response({"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        # Get StudentProfile by user_id via StudentSchool relation
        student_school = StudentSchool.objects.get(user_id=user_id)
        profile = StudentProfile.objects.get(student=student_school)
    except (StudentSchool.DoesNotExist, StudentProfile.DoesNotExist):
        return Response({"detail": "Student profile not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = StudentProfileSerializer(profile)
    return Response(serializer.data, status=status.HTTP_200_OK)






@swagger_auto_schema(
    method='post',
    operation_summary="Create Student Profile",
    operation_description="Create a student profile for the given user ID.",
    request_body=StudentProfileSerializer(),
    responses={
        201: openapi.Response('Student profile created', StudentProfileSerializer()),
        400: 'Invalid input',
        403: 'Permission denied',
        404: 'StudentSchool not found',
    },
    manual_parameters=[
        openapi.Parameter(
            'Authorization',
            openapi.IN_HEADER,
            description='Authorization token',
            type=openapi.TYPE_STRING,
            required=True
        ),
        openapi.Parameter(
            'user_id',
            openapi.IN_PATH,
            description='ID of the user to create profile for',
            type=openapi.TYPE_STRING,
            required=True
        ),
    ]
)
@api_view(['POST'])
@permission_classes([AllowAny])
def create_student_profile(request, user_id):
    user, error_response = get_user_from_token(request)
    if error_response:
        return error_response

    if str(user.id) != str(user_id):
        return Response({"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        student_school = StudentSchool.objects.get(user_id=user_id)
    except StudentSchool.DoesNotExist:
        return Response({"detail": "StudentSchool not found"}, status=status.HTTP_404_NOT_FOUND)

    data = request.data.copy()
    data['student'] = student_school.id  # assign FK

    serializer = StudentProfileSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







@swagger_auto_schema(
    method='put',
    operation_summary="Update Student Profile",
    operation_description="Update the student profile for the given user ID.",
    request_body=StudentProfileSerializer(),
    responses={
        200: openapi.Response('Student profile updated', StudentProfileSerializer()),
        400: 'Invalid input',
        403: 'Permission denied',
        404: 'Student profile not found',
    },
    manual_parameters=[
        openapi.Parameter(
            'Authorization',
            openapi.IN_HEADER,
            description='Authorization token',
            type=openapi.TYPE_STRING,
            required=True
        ),
        openapi.Parameter(
            'user_id',
            openapi.IN_PATH,
            description='ID of the user to update profile for',
            type=openapi.TYPE_STRING,
            required=True
        ),
    ]
)
@api_view(['PUT'])
@permission_classes([AllowAny])
def update_student_profile(request, user_id):
    user, error_response = get_user_from_token(request)
    if error_response:
        return error_response

    if str(user.id) != str(user_id):
        return Response({"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        student_school = StudentSchool.objects.get(user_id=user_id)
        profile = StudentProfile.objects.get(student=student_school)
    except (StudentSchool.DoesNotExist, StudentProfile.DoesNotExist):
        return Response({"detail": "Student profile not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = StudentProfileSerializer(profile, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






@swagger_auto_schema(
    method='delete',
    operation_summary="Delete Student Profile",
    operation_description="Delete the student profile for the given user ID.",
    responses={
        204: 'Deleted successfully',
        403: 'Permission denied',
        404: 'Student profile not found',
    },
    manual_parameters=[
        openapi.Parameter(
            'Authorization',
            openapi.IN_HEADER,
            description='Authorization token',
            type=openapi.TYPE_STRING,
            required=True
        ),
        openapi.Parameter(
            'user_id',
            openapi.IN_PATH,
            description='ID of the user to delete profile for',
            type=openapi.TYPE_STRING,
            required=True
        ),
    ]
)
@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_student_profile(request, user_id):
    user, error_response = get_user_from_token(request)
    if error_response:
        return error_response

    if str(user.id) != str(user_id):
        return Response({"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        student_school = StudentSchool.objects.get(user_id=user_id)
        profile = StudentProfile.objects.get(student=student_school)
        profile.delete()
        return Response({"detail": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except (StudentSchool.DoesNotExist, StudentProfile.DoesNotExist):
        return Response({"detail": "Student profile not found"}, status=status.HTTP_404_NOT_FOUND)
    
    
    

@swagger_auto_schema(
    method='get',
    operation_summary="Student Dashboard",
    operation_description="Get dashboard data for a student including subject completion and recent incomplete topics.",
    responses={
        200: openapi.Response(
            'Dashboard data',
            schema=SubjectDashboardResponseSerializer()  # ✅ Create a wrapper serializer for the response
        ),
        401: 'Token missing or unauthorized',
        404: 'Student or class not found',
    },
    manual_parameters=[
        openapi.Parameter(
            'Authorization',
            openapi.IN_HEADER,
            description='Authorization token',
            type=openapi.TYPE_STRING,
            required=True
        ),
        openapi.Parameter(
            'user_id',
            openapi.IN_PATH,
            description='ID of the student user',
            type=openapi.TYPE_STRING,
            required=True
        ),
        openapi.Parameter(
            'account_type',
            openapi.IN_PATH,
            description='Account type of the student',
            type=openapi.TYPE_STRING,
            required=True
        ),
    ]
)

@api_view(['GET'])
@permission_classes([AllowAny])
def student_dashboard(request, user_id, account_type):
    # Token Auth manually
    token = request.headers.get('Authorization')
    if not token:
        return Response({'error': 'Token missing'}, status=401)
    
    try:
        user = CustomUser.objects.get(id=user_id, role='student', account_type=account_type)
    except CustomUser.DoesNotExist:
        return Response({'error': 'Student not found'}, status=404)

    # Get student's assigned class
    try:
        student_school = StudentSchool.objects.get(user=user)
        student_class = student_school.class_assigned
    except StudentSchool.DoesNotExist:
        return Response({'error': 'Student class not assigned'}, status=404)

    # Subject-wise completion calculation
    subjects = Subject.objects.filter(assigned_class=student_class)
    subject_data = []

    for subject in subjects:
        chapters = Chapter.objects.filter(subject=subject)
        total_topics = 0
        total_completion = 0

        for chapter in chapters:
            topics = Topic.objects.filter(chapter=chapter)
            for topic in topics:
                total_topics += 1
                progress = TopicProgress.objects.filter(student=user, topic=topic).first()
                if progress:
                    total_completion += float(progress.completion_percentage)

        if total_topics > 0:
            completion_percentage = round(total_completion / total_topics, 2)
        else:
            completion_percentage = 0.0

        subject_data.append({
            'subject_name': subject.name,
            'completion_percentage': completion_percentage,
        })

    subject_serializer = SubjectCompletionSerializer(subject_data, many=True)

    # Incomplete topics in last 24h
    twenty_four_hours_ago = timezone.now() - timedelta(hours=24)
    incomplete_topics = TopicProgress.objects.filter(
        student=user,
        is_completed=False,
        last_accessed__gte=twenty_four_hours_ago,
        completion_percentage__gt=0
    )

    incomplete_topic_data = []
    for tp in incomplete_topics:
        chapter = tp.topic.chapter
        subject = chapter.subject
        incomplete_topic_data.append({
            'topic_name': tp.topic.name,
            'subject_name': subject.name,
            'chapter_name': chapter.name,
            'completion_percentage': tp.completion_percentage,
            'last_accessed': tp.last_accessed,
        })

    incomplete_serializer = IncompleteTopicSerializer(incomplete_topic_data, many=True)

    return Response({
        'subjects': subject_serializer.data,
        'recent_incomplete_topics': incomplete_serializer.data,
    }, status=200)
    
    




@swagger_auto_schema(
    method='get',
    operation_summary="Get Student Subjects",
    operation_description="Retrieve the list of subjects assigned to the student's class.",
    responses={
        200: openapi.Response('Subjects list', SubjectSerializer(many=True)),
        401: 'Authorization token missing',
        404: 'Student or class not assigned',
    },
    manual_parameters=[
        openapi.Parameter(
            'Authorization',
            openapi.IN_HEADER,
            description='Authorization token',
            type=openapi.TYPE_STRING,
            required=True
        ),
        openapi.Parameter(
            'user_id',
            openapi.IN_PATH,
            description='ID of the student user',
            type=openapi.TYPE_STRING,
            required=True
        ),
    ]
)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_student_subjects(request, user_id):
    token = request.headers.get('Authorization')
    if not token:
        return Response({'error': 'Authorization token missing'}, status=401)

    try:
        user = CustomUser.objects.get(id=user_id, role='student')
    except CustomUser.DoesNotExist:
        return Response({'error': 'Student not found'}, status=404)

    try:
        student_school = StudentSchool.objects.get(user=user)
    except StudentSchool.DoesNotExist:
        return Response({'error': 'Student class not assigned'}, status=404)

    subjects = Subject.objects.filter(assigned_class=student_school.class_assigned)
    serializer = SubjectSerializer(subjects, many=True)
    return Response(serializer.data, status=200)








@swagger_auto_schema(
    method='get',
    operation_summary="Get Subject Chapters With Progress",
    operation_description="Retrieve chapters of a subject with topic progress for the given student.",
    responses={
        200: openapi.Response('Chapters with progress', ChapterWithTopicsSerializer(many=True)),
        403: 'Permission denied',
        404: 'Subject not found',
    },
    manual_parameters=[
        openapi.Parameter(
            'Authorization',
            openapi.IN_HEADER,
            description='Authorization token',
            type=openapi.TYPE_STRING,
            required=True
        ),
        openapi.Parameter(
            'subject_id',
            openapi.IN_PATH,
            description='ID of the subject',
            type=openapi.TYPE_STRING,
            required=True
        ),
        openapi.Parameter(
            'user_id',
            openapi.IN_PATH,
            description='ID of the student user',
            type=openapi.TYPE_STRING,
            required=True
        ),
    ]
)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_subject_chapters_with_progress(request, subject_id, user_id):
    user, error_response = get_user_from_token(request)
    if error_response:
        return error_response
    
    # Optionally, check if user_id matches token user or if user has permission
    if str(user.id) != str(user_id):
        return Response({"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        subject = Subject.objects.get(id=subject_id)
    except Subject.DoesNotExist:
        return Response({'error': 'Subject not found'}, status=HTTP_404_NOT_FOUND)

    chapters = Chapter.objects.filter(subject=subject)
    serializer = ChapterWithTopicsSerializer(chapters, many=True, context={'user': user})
    return Response(serializer.data, status=200)














    