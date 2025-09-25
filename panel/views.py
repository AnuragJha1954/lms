from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from v1.models import Subject, Chapter, Topic, Content, ClassModel
from .serializers import SubjectSerializer, ChapterSerializer, TopicSerializer, ContentSerializer, AssignStudentSerializer, ClassModelSerializer

# ----------- SUBJECT CRUD -----------

@swagger_auto_schema(method='get', operation_summary="List all subjects")
@swagger_auto_schema(method='post', operation_summary="Create a new subject", request_body=SubjectSerializer)
@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def subject_list_create(request):
    if request.method == "GET":
        subjects = Subject.objects.all()
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = SubjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='get', operation_summary="Retrieve a subject by ID")
@swagger_auto_schema(method='put', operation_summary="Update a subject by ID", request_body=SubjectSerializer)
@swagger_auto_schema(method='delete', operation_summary="Delete a subject by ID")
@api_view(["GET", "PUT", "DELETE"])
@permission_classes([AllowAny])
def subject_detail(request, pk):
    try:
        subject = Subject.objects.get(pk=pk)
    except Subject.DoesNotExist:
        return Response({"error": "Subject not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = SubjectSerializer(subject)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = SubjectSerializer(subject, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        subject.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ----------- CHAPTER CRUD -----------

@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def chapter_list_create(request):
    if request.method == "GET":
        chapters = Chapter.objects.all()
        serializer = ChapterSerializer(chapters, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = ChapterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([AllowAny])
def chapter_detail(request, pk):
    try:
        chapter = Chapter.objects.get(pk=pk)
    except Chapter.DoesNotExist:
        return Response({"error": "Chapter not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ChapterSerializer(chapter)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = ChapterSerializer(chapter, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        chapter.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ----------- TOPIC CRUD -----------

@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def topic_list_create(request):
    if request.method == "GET":
        topics = Topic.objects.all()
        serializer = TopicSerializer(topics, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = TopicSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([AllowAny])
def topic_detail(request, pk):
    try:
        topic = Topic.objects.get(pk=pk)
    except Topic.DoesNotExist:
        return Response({"error": "Topic not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = TopicSerializer(topic)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = TopicSerializer(topic, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        topic.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ----------- CONTENT CRUD -----------

@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def content_list_create(request):
    if request.method == "GET":
        contents = Content.objects.all()
        serializer = ContentSerializer(contents, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = ContentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([AllowAny])
def content_detail(request, pk):
    try:
        content = Content.objects.get(pk=pk)
    except Content.DoesNotExist:
        return Response({"error": "Content not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ContentSerializer(content)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = ContentSerializer(content, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        content.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




@swagger_auto_schema(
    method="post",
    request_body=AssignStudentSerializer,
    responses={200: "Students assigned successfully", 400: "Invalid data"},
    operation_description="Assign one or multiple students to a subject"
)
@api_view(["POST"])
@permission_classes([])
def assign_students_to_subject(request, subject_id):
    try:
        subject = Subject.objects.get(id=subject_id)
    except Subject.DoesNotExist:
        return Response({"error": "Subject not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = AssignStudentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(subject=subject)
        return Response({"message": "Students assigned successfully"}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






# Create a class
@swagger_auto_schema(
    method='post',
    request_body=ClassModelSerializer,
    responses={201: ClassModelSerializer, 400: 'Bad Request'}
)
@api_view(['POST'])
def create_class(request):
    serializer = ClassModelSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# List all classes
@swagger_auto_schema(
    method='get',
    responses={200: ClassModelSerializer(many=True)}
)
@api_view(['GET'])
def list_classes(request):
    classes = ClassModel.objects.all()
    serializer = ClassModelSerializer(classes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Retrieve a single class by ID
@swagger_auto_schema(
    method='get',
    responses={200: ClassModelSerializer, 404: 'Not Found'}
)
@api_view(['GET'])
def retrieve_class(request, class_id):
    try:
        cls = ClassModel.objects.get(id=class_id)
    except ClassModel.DoesNotExist:
        return Response({"error": "Class not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = ClassModelSerializer(cls)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Update a class
@swagger_auto_schema(
    method='put',
    request_body=ClassModelSerializer,
    responses={200: ClassModelSerializer, 400: 'Bad Request', 404: 'Not Found'}
)
@swagger_auto_schema(
    method='patch',
    request_body=ClassModelSerializer,
    responses={200: ClassModelSerializer, 400: 'Bad Request', 404: 'Not Found'}
)
@api_view(['PUT', 'PATCH'])
def update_class(request, class_id):
    try:
        cls = ClassModel.objects.get(id=class_id)
    except ClassModel.DoesNotExist:
        return Response({"error": "Class not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = ClassModelSerializer(cls, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Delete a class
@swagger_auto_schema(
    method='delete',
    responses={204: 'No Content', 404: 'Not Found'}
)
@api_view(['DELETE'])
def delete_class(request, class_id):
    try:
        cls = ClassModel.objects.get(id=class_id)
    except ClassModel.DoesNotExist:
        return Response({"error": "Class not found"}, status=status.HTTP_404_NOT_FOUND)

    cls.delete()
    return Response({"message": "Class deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


