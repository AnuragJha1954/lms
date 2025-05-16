from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from v1.utils import (
    update_topic_progress, 
    get_user_from_token
)

from v1.models import (
    Content
)

from users.models import CustomUser

from v1.serializers import (
    ContentCompleteSerializer
)


@swagger_auto_schema(
    method='put',
    operation_summary="Mark Content as Completed",
    operation_description="Mark a specific content item as completed by the student.",
    manual_parameters=[
        openapi.Parameter(
            name='Authorization',
            in_=openapi.IN_HEADER,
            description='Token authorization header: "Authorization: token <your_token>"',
            type=openapi.TYPE_STRING,
            required=True
        ),
        openapi.Parameter(
            name='content_id',
            in_=openapi.IN_PATH,
            description='ID of the content to mark as completed',
            type=openapi.TYPE_INTEGER,
            required=True
        ),
    ],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'completed': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Completion status (true to mark completed)'),
        },
        required=['completed']
    ),
    responses={
        200: openapi.Response(description="Content marked as completed"),
        400: openapi.Response(description="Invalid input"),
        404: openapi.Response(description="Content not found"),
        401: openapi.Response(description="Unauthorized"),
    },
)
@api_view(['PUT'])
@permission_classes([AllowAny])
def mark_content_completed(request, content_id):
    user, error = get_user_from_token(request)
    if error:
        return error

    try:
        content = Content.objects.get(id=content_id)
    except Content.DoesNotExist:
        return Response({"detail": "Content not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = ContentCompleteSerializer(content, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        update_topic_progress(user, content.topic)
        return Response({"detail": "Content marked as completed", "data": serializer.data}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
