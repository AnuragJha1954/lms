from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from school.models import SchoolProfile
from v1.models import TeacherSubjectAssignment
from teachers.models import TeacherProfile
from students.models import StudentProfile, StudentClassAssignment
from teachers.serializers import TeacherCreateSerializer
from students.serializers import StudentCreateSerializer
from .serializers import SchoolRegistrationSerializer, ClassWithSubjectsSerializer, TeacherSubjectAssignSerializer, AssignStudentToClassSerializer, SchoolProfileSerializer, StudentProfileSerializer
from users.models import CustomUser


@swagger_auto_schema(
    method='post',
    request_body=SchoolRegistrationSerializer,
    operation_summary="Register School",
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
    operation_summary="Update Teacher Details",
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




@swagger_auto_schema(
    method='delete',
    operation_summary="Delete a teacher",
    manual_parameters=[
        openapi.Parameter(
            'school_id',
            openapi.IN_PATH,
            description="ID of the school",
            type=openapi.TYPE_INTEGER,
            required=True
        ),
        openapi.Parameter(
            'teacher_id',
            openapi.IN_PATH,
            description="ID of the teacher to be deleted",
            type=openapi.TYPE_INTEGER,
            required=True
        ),
    ],
    responses={
        204: openapi.Response(description="Teacher deleted successfully."),
        404: openapi.Response(description="School or Teacher not found."),
    }
)
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
    operation_summary="Update the Student Details by school",
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







@swagger_auto_schema(
    method='delete',
    operation_summary="Delete a student",
    manual_parameters=[
        openapi.Parameter(
            'school_id',
            openapi.IN_PATH,
            description="ID of the school",
            type=openapi.TYPE_INTEGER,
            required=True
        ),
        openapi.Parameter(
            'student_id',
            openapi.IN_PATH,
            description="ID of the student to be deleted",
            type=openapi.TYPE_INTEGER,
            required=True
        ),
    ],
    responses={
        204: openapi.Response(description="Student deleted successfully."),
        404: openapi.Response(description="School or Student not found."),
    }
)
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
    operation_summary="Add classes with Subjects",
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
    operation_summary="Assign subject ot the teacher",
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
    operation_summary="Assign the student to the class",
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
    operation_summary="Get the School Profile details",
    manual_parameters=[
        openapi.Parameter('school_user_id', openapi.IN_PATH, description="User ID of the school", type=openapi.TYPE_INTEGER)
    ],
    responses={200: SchoolProfileSerializer()}
)
@swagger_auto_schema(
    method='put',
    operation_summary="Update the school Profile",
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
    
    




@swagger_auto_schema(
    method='get',
    operation_summary="Get students by school ID",
    manual_parameters=[
        openapi.Parameter(
            'school_id',
            openapi.IN_PATH,
            description="ID of the school",
            type=openapi.TYPE_INTEGER,
            required=True
        )
    ],
    responses={
        200: openapi.Response(
            description="List of students in the school",
            examples={
                "application/json": [
                    {
                        "id": 1,
                        "user": {
                            "id": 101,
                            "first_name": "Rahul",
                            "last_name": "Verma",
                            "email": "rahul@example.com"
                        },
                        "roll_number": "A102",
                        "guardian_name": "Ramesh Verma",
                        "contact_number": "9876543210",
                        "date_of_birth": "2010-06-15",
                        "gender": "Male",
                        "address": "Sector 15, Delhi",
                        "class": "Class 8",
                        "gpa": 8.5
                    },
                    {
                        "id": 2,
                        "user": {
                            "id": 102,
                            "first_name": "Aisha",
                            "last_name": "Khan",
                            "email": "aisha@example.com"
                        },
                        "roll_number": "B203",
                        "guardian_name": "Firoz Khan",
                        "contact_number": "9123456789",
                        "date_of_birth": "2009-12-20",
                        "gender": "Female",
                        "address": "Andheri East, Mumbai",
                        "class": "Class 9",
                        "gpa": 8.5
                    }
                ]
            }
        ),
        404: openapi.Response(
            description="School not found",
            examples={
                "application/json": {"error": "School not found."}
            }
        )
    },
    operation_description="Retrieve all students belonging to a specific school by school ID, including their class and GPA."
)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_students_by_school(request, school_id):
    try:
        # Check if school exists
        school = SchoolProfile.objects.get(id=school_id)
    except SchoolProfile.DoesNotExist:
        return Response({'error': 'School not found.'}, status=status.HTTP_404_NOT_FOUND)

    # Get all students for this school
    students = StudentProfile.objects.filter(school=school)

    # Summary counts (assuming 'status' field exists in StudentProfile)
    total_students = students.count()
    # active_students = students.filter(status="active").count()
    # inactive_students = students.filter(status="inactive").count()
    # pending_students = students.filter(status="pending").count()
    # rejected_students = students.filter(status="rejected").count()
    active_students = students.count()
    inactive_students = 0
    pending_students = 0
    rejected_students = 0

    # Serialize student data
    serializer = StudentProfileSerializer(students, many=True)

    # Enrich student data with class name and GPA
    enriched_data = []
    for student_data in serializer.data:
        student_id = student_data['id']
        try:
            assignment = StudentClassAssignment.objects.get(student_id=student_id)
            class_name = assignment.class_model.class_name
        except StudentClassAssignment.DoesNotExist:
            class_name = None

        student_data['class'] = class_name
        student_data['gpa'] = 8.5  # Hardcoded GPA

        enriched_data.append(student_data)

    return Response({
        "status": True,
        "total_students": total_students,
        "active_students": active_students,
        "inactive_students": inactive_students,
        "pending_students": pending_students,
        "rejected_students": rejected_students,
        "students": enriched_data
    }, status=status.HTTP_200_OK)







@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter(
            'school_id',
            openapi.IN_PATH,
            description="ID of the school",
            type=openapi.TYPE_INTEGER
        )
    ],
    operation_summary="Get teachers by school ID",
    operation_description="Returns all teachers in a given school with their profile and assigned subjects.",
    responses={
        200: openapi.Response(
            description="List of teachers with assigned subjects",
            examples={
                "application/json": [
                    {
                        "id": 1,
                        "full_name": "Anita Sharma",
                        "email": "anita@example.com",
                        "phone_number": "9876543210",
                        "qualification": "M.Sc, B.Ed",
                        "gender": "female",
                        "date_of_birth": "1985-06-20",
                        "experience_years": 10,
                        "subject_specialization": "Physics",
                        "address": "Delhi",
                        "profile_picture": "http://yourdomain.com/media/teacher_profiles/anita.jpg",
                        "assigned_subjects": ["Physics", "Mathematics"]
                    }
                ]
            }
        ),
        404: openapi.Response(description="School not found")
    }
)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_teachers_by_school(request, school_id):
    try:
        school = SchoolProfile.objects.get(id=school_id)
    except SchoolProfile.DoesNotExist:
        return Response({"error": "School not found"}, status=status.HTTP_404_NOT_FOUND)

    teachers = TeacherProfile.objects.filter(school=school)

    teacher_data = []
    total_experience = 0
    subject_set = set()

    for teacher in teachers:
        subject_assignments = TeacherSubjectAssignment.objects.filter(teacher=teacher)
        subjects = [assignment.subject.name for assignment in subject_assignments]
        subject_set.update(subjects)

        total_experience += teacher.experience_years or 0

        teacher_data.append({
            "id": teacher.id,
            "full_name": teacher.user.full_name,
            "email": teacher.user.email,
            "phone_number": teacher.phone_number,
            "qualification": teacher.qualification,
            "gender": teacher.gender,
            "date_of_birth": teacher.date_of_birth,
            "experience_years": teacher.experience_years,
            "subject_specialization": teacher.subject_specialization,
            "address": teacher.address,
            "profile_picture": request.build_absolute_uri(teacher.profile_picture.url) if teacher.profile_picture else None,
            "assigned_subjects": subjects,
        })

    response_data = {
        "status": True,
        "total_teachers": teachers.count(),
        "total_experience": total_experience,
        "total_departments": len(subject_set),
        "experience_avg": 5,  # Hardcoded value
        "teachers": teacher_data,
    }

    return Response(response_data, status=status.HTTP_200_OK)










@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter(
            'school_id',
            openapi.IN_PATH,
            type=openapi.TYPE_INTEGER,
            description="ID of the school"
        ),
        openapi.Parameter(
            'teacher_id',
            openapi.IN_PATH,
            type=openapi.TYPE_INTEGER,
            description="ID of the teacher"
        ),
    ],
    operation_summary="Get a teacher's details by school and teacher ID",
    operation_description="Returns detailed information about a specific teacher, including name, email, phone, subjects assigned, and classes assigned.",
    responses={
        200: openapi.Response(
            description="Teacher profile data with subjects and classes",
            examples={
                "application/json": {
                    "id": 3,
                    "full_name": "Anita Sharma",
                    "email": "anita.sharma@example.com",
                    "phone_number": "9876543210",
                    "qualification": "M.Sc, B.Ed",
                    "gender": "Female",
                    "date_of_birth": "1985-06-15",
                    "experience_years": 10,
                    "subject_specialization": "Mathematics",
                    "address": "123 Sector 4, Delhi",
                    "profile_picture": "http://example.com/media/teachers/profile/anita.jpg",
                    "assigned_subjects": [
                        {
                            "subject_id": 5,
                            "name": "Mathematics",
                            "class": "Class 10-A (2024-2025)"
                        },
                        {
                            "subject_id": 7,
                            "name": "Physics",
                            "class": "Class 10-B (2024-2025)"
                        }
                    ],
                    "assigned_classes": [
                        {
                            "class_id": 2,
                            "name": "Class 10",
                            "section": "A",
                            "academic_year": "2024-2025"
                        },
                        {
                            "class_id": 3,
                            "name": "Class 10",
                            "section": "B",
                            "academic_year": "2024-2025"
                        }
                    ]
                }
            }
        ),
        404: openapi.Response(
            description="Teacher or School not found",
            examples={
                "application/json": {
                    "error": "Teacher not found in this school"
                }
            }
        )
    }
)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_teacher_details(request, school_id, teacher_id):
    try:
        school = SchoolProfile.objects.get(id=school_id)
    except SchoolProfile.DoesNotExist:
        return Response({"error": "School not found"}, status=status.HTTP_404_NOT_FOUND)

    try:
        teacher = TeacherProfile.objects.get(id=teacher_id, school=school)
    except TeacherProfile.DoesNotExist:
        return Response({"error": "Teacher not found in this school"}, status=status.HTTP_404_NOT_FOUND)

    # Assigned subjects
    subject_assignments = TeacherSubjectAssignment.objects.filter(teacher=teacher)
    subjects = [
        {
            "subject_id": assignment.subject.id,
            "name": assignment.subject.name,
            "class": str(assignment.subject.class_model),
        }
        for assignment in subject_assignments
    ]

    # Assigned classes from ManyToMany field
    classes = [
        {
            "class_id": class_obj.id,
            "name": class_obj.class_name,
            "section": class_obj.section,
            "academic_year": class_obj.academic_year
        }
        for class_obj in teacher.assigned_classes.all()
    ]

    data = {
        "id": teacher.id,
        "full_name": teacher.user.full_name,
        "email": teacher.user.email,
        "phone_number": teacher.phone_number,
        "qualification": teacher.qualification,
        "gender": teacher.gender,
        "date_of_birth": teacher.date_of_birth,
        "experience_years": teacher.experience_years,
        "subject_specialization": teacher.subject_specialization,
        "address": teacher.address,
        "profile_picture": request.build_absolute_uri(teacher.profile_picture.url) if teacher.profile_picture else None,
        "assigned_subjects": subjects,
        "assigned_classes": classes,
    }

    return Response(data, status=status.HTTP_200_OK)






@swagger_auto_schema(
    method='get',
    operation_summary="Get dashboard data for school",
    manual_parameters=[
        openapi.Parameter(
            'school_user_id',
            openapi.IN_PATH,
            description="ID of the school user",
            type=openapi.TYPE_INTEGER,
            required=True
        ),
    ],
    responses={
        200: openapi.Response(
            description="Dashboard data for school",
            examples={
                "application/json": {
                    "status": True,
                    "data": {
                        "school": "Springfield High",
                        "total_students": 350,
                        "total_teachers": 25,
                        "average_performance": 82,
                        "attendance_rate": 95,
                        "performance_by_subject": [
                            {"subject": "Math", "average": 85},
                            {"subject": "Science", "average": 75},
                            {"subject": "English", "average": 78},
                            {"subject": "History", "average": 72},
                            {"subject": "Arts", "average": 88}
                        ],
                        "grade_distribution": {
                            "A": 45,
                            "B": 78,
                            "C": 65,
                            "D": 25,
                            "F": 12
                        },
                        "monthly_trends": [
                            {"month": "Jan", "attendance": 90, "performance": 85},
                            {"month": "Feb", "attendance": 88, "performance": 87},
                            {"month": "Mar", "attendance": 92, "performance": 90},
                            {"month": "Apr", "attendance": 89, "performance": 88},
                            {"month": "May", "attendance": 93, "performance": 91},
                            {"month": "Jun", "attendance": 94, "performance": 92}
                        ]
                    }
                }
            }
        ),
        404: "School not found"
    }
)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_dashboard_data(request, school_user_id):
    try:
        school_user = CustomUser.objects.get(id=school_user_id, role="school")
        school = SchoolProfile.objects.get(user=school_user)
    except (CustomUser.DoesNotExist, SchoolProfile.DoesNotExist):
        return Response({"status": False, "message": "School not found"}, status=404)

    # Fetch counts
    total_students = StudentProfile.objects.filter(school=school).count()
    total_teachers = TeacherProfile.objects.filter(school=school).count()

    # Hardcoded values for now
    average_performance = 82
    attendance_rate = 95

    # Example subject performance (could be calculated dynamically later)
    performance_by_subject = [
        {"subject": "Math", "average": 85},
        {"subject": "Science", "average": 75},
        {"subject": "English", "average": 78},
        {"subject": "History", "average": 72},
        {"subject": "Arts", "average": 88},
    ]

    # Example grade distribution
    grade_distribution = {
        "A": 45,
        "B": 78,
        "C": 65,
        "D": 25,
        "F": 12,
    }

    # Example monthly trends (attendance & performance over 6 months)
    monthly_trends = [
        {"month": "Jan", "attendance": 90, "performance": 85},
        {"month": "Feb", "attendance": 88, "performance": 87},
        {"month": "Mar", "attendance": 92, "performance": 90},
        {"month": "Apr", "attendance": 89, "performance": 88},
        {"month": "May", "attendance": 93, "performance": 91},
        {"month": "Jun", "attendance": 94, "performance": 92},
    ]

    data = {
        "school": school.name,
        "total_students": total_students,
        "total_teachers": total_teachers,
        "average_performance": average_performance,
        "attendance_rate": attendance_rate,
        "performance_by_subject": performance_by_subject,
        "grade_distribution": grade_distribution,
        "monthly_trends": monthly_trends,
    }

    return Response({"status": True, "data": data}, status=200)






