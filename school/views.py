from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from school.models import SchoolProfile
from teachers.models import TeacherProfile
from students.models import StudentProfile
from teachers.serializers import TeacherCreateSerializer
from students.serializers import StudentCreateSerializer
from .serializers import SchoolRegistrationSerializer, ClassWithSubjectsSerializer, TeacherSubjectAssignSerializer, AssignStudentToClassSerializer, SchoolProfileSerializer
from users.models import CustomUser


@swagger_auto_schema(
    method='post',
    request_body=SchoolRegistrationSerializer,
    responses={
        201: openapi.Response('School created successfully', SchoolRegistrationSerializer),
        400: 'Bad Request'
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def register_school(request):
    serializer = SchoolRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        school = serializer.save()
        return Response(SchoolRegistrationSerializer(school).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






@swagger_auto_schema(
    method='put',
    request_body=TeacherCreateSerializer,
    responses={200: "Teacher updated", 404: "Not Found"}
)
@api_view(['PUT'])
@permission_classes([AllowAny])
def update_teacher(request, school_id, teacher_id):
    try:
        school = SchoolProfile.objects.get(id=school_id)
    except SchoolProfile.DoesNotExist:
        return Response({"error": "School not found."}, status=status.HTTP_404_NOT_FOUND)

    try:
        teacher = TeacherProfile.objects.get(id=teacher_id, school=school)
    except TeacherProfile.DoesNotExist:
        return Response({"error": "Teacher not found for this school."}, status=status.HTTP_404_NOT_FOUND)

    serializer = TeacherCreateSerializer(teacher, data=request.data, partial=True, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_teacher(request, school_id, teacher_id):
    try:
        school = SchoolProfile.objects.get(id=school_id)
    except SchoolProfile.DoesNotExist:
        return Response({"error": "School not found."}, status=status.HTTP_404_NOT_FOUND)

    try:
        teacher = TeacherProfile.objects.get(id=teacher_id, school=school)
    except TeacherProfile.DoesNotExist:
        return Response({"error": "Teacher not found for this school."}, status=status.HTTP_404_NOT_FOUND)

    # Delete associated user first
    if teacher.user:
        teacher.user.delete()

    teacher.delete()

    return Response({"message": "Teacher deleted successfully."}, status=status.HTTP_204_NO_CONTENT)






@swagger_auto_schema(
    method='put',
    request_body=StudentCreateSerializer,
    responses={
        200: "Student updated successfully.",
        404: "Student not found."
    }
)
@api_view(['PUT'])
@permission_classes([AllowAny])
def update_student(request, school_id, student_id):
    try:
        school = SchoolProfile.objects.get(id=school_id)
    except SchoolProfile.DoesNotExist:
        return Response({"error": "School not found."}, status=status.HTTP_404_NOT_FOUND)

    try:
        student = StudentProfile.objects.get(id=student_id, school=school)
    except StudentProfile.DoesNotExist:
        return Response({"error": "Student not found for this school."}, status=status.HTTP_404_NOT_FOUND)

    serializer = StudentCreateSerializer(student, data=request.data, partial=True, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)








@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_student(request, school_id, student_id):
    try:
        school = SchoolProfile.objects.get(id=school_id)
    except SchoolProfile.DoesNotExist:
        return Response({"error": "School not found."}, status=status.HTTP_404_NOT_FOUND)

    try:
        student = StudentProfile.objects.get(id=student_id, school=school)
    except StudentProfile.DoesNotExist:
        return Response({"error": "Student not found for this school."}, status=status.HTTP_404_NOT_FOUND)

    if student.user:
        student.user.delete()

    student.delete()
    return Response({"message": "Student deleted successfully."}, status=status.HTTP_204_NO_CONTENT)





# {
#   "school_id": 1,
#   "class_name": "Class 10",
#   "section": "A",
#   "academic_year": "2025-2026",
#   "subjects": [
#     { "name": "Math", "code": "MTH101" },
#     { "name": "Science", "code": "SCI101" }
#   ]
# }



@swagger_auto_schema(
    method='post',
    request_body=ClassWithSubjectsSerializer,
    responses={201: "Class and subjects created", 400: "Validation error"},
    manual_parameters=[
        openapi.Parameter('school_user_id', openapi.IN_PATH, description="School user ID", type=openapi.TYPE_INTEGER)
    ]
)
@api_view(['POST'])
@permission_classes([AllowAny])
def add_class_with_subjects(request, school_user_id):
    try:
        school_user = CustomUser.objects.get(id=school_user_id, role='school')
        school = school_user.school_profile
    except CustomUser.DoesNotExist:
        return Response({"error": "School user not found."}, status=status.HTTP_404_NOT_FOUND)
    except SchoolProfile.DoesNotExist:
        return Response({"error": "School profile not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = ClassWithSubjectsSerializer(data=request.data, context={'school': school})
    if serializer.is_valid():
        created_class = serializer.save()
        return Response({"message": "Class and subjects created", "class_id": created_class.id}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






# {
#   "teacher_id": 5,
#   "subject_id": 12
# }




@swagger_auto_schema(
    method='post',
    request_body=TeacherSubjectAssignSerializer,
    responses={201: "Teacher assigned to subject", 400: "Bad request"}
)
@api_view(['POST'])
@permission_classes([AllowAny])
def assign_teacher_to_subject(request):
    serializer = TeacherSubjectAssignSerializer(data=request.data)
    if serializer.is_valid():
        assignment = serializer.save()
        return Response({"message": "Teacher assigned", "assignment_id": assignment.id}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)










@swagger_auto_schema(
    method='post',
    request_body=AssignStudentToClassSerializer,
    responses={201: "Student assigned to class", 400: "Bad request"}
)
@api_view(['POST'])
@permission_classes([AllowAny])
def assign_student_to_class(request):
    serializer = AssignStudentToClassSerializer(data=request.data)
    if serializer.is_valid():
        assignment = serializer.save()
        return Response({
            "message": "Student assigned to class successfully.",
            "student_id": assignment.student.id,
            "class_id": assignment.class_model.id
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('school_user_id', openapi.IN_PATH, description="User ID of the school", type=openapi.TYPE_INTEGER)
    ],
    responses={200: SchoolProfileSerializer()}
)
@swagger_auto_schema(
    method='put',
    request_body=SchoolProfileSerializer,
    responses={200: SchoolProfileSerializer(), 400: "Validation error", 404: "School not found"}
)
@api_view(['GET', 'PUT'])
@permission_classes([AllowAny])
def manage_school_profile(request, school_user_id):
    try:
        school_user = CustomUser.objects.get(id=school_user_id, role='school')
        school_profile = school_user.school_profile
    except CustomUser.DoesNotExist:
        return Response({"error": "School user not found."}, status=status.HTTP_404_NOT_FOUND)
    except SchoolProfile.DoesNotExist:
        return Response({"error": "School profile not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SchoolProfileSerializer(school_profile)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SchoolProfileSerializer(school_profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)