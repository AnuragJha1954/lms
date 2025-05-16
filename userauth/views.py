from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import (
    LoginSerializer
)

from users.models import CustomUser


@swagger_auto_schema(
    method='post',
    operation_summary="User Login",
    operation_description="Authenticate user and get token along with user details.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['email', 'password'],
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, format='email', description='User email'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, format='password', description='User password'),
        }
    ),
    responses={
        200: openapi.Response(
            description="Login successful",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'token': openapi.Schema(type=openapi.TYPE_STRING),
                    'user': openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'email': openapi.Schema(type=openapi.TYPE_STRING),
                            'role': openapi.Schema(type=openapi.TYPE_STRING),
                            'account_type': openapi.Schema(type=openapi.TYPE_STRING),
                            'name': openapi.Schema(type=openapi.TYPE_STRING),
                        }
                    ),
                }
            )
        ),
        400: openapi.Response(description="Invalid credentials or input"),
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "token": token.key,
            "user": {
                "id": user.id,
                "email": user.email,
                "role": user.role,
                "account_type": user.account_type,
                "name": user.get_full_name() if hasattr(user, 'get_full_name') else user.username,
            }
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






@swagger_auto_schema(
    method='post',
    operation_summary="User Logout",
    operation_description="Invalidate the current token to logout the user.",
    manual_parameters=[
        openapi.Parameter(
            'Authorization',
            openapi.IN_HEADER,
            description='Token authorization header: "Authorization: token <your_token>"',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    responses={
        200: openapi.Response(description="Logged out successfully"),
        401: openapi.Response(description="Unauthorized"),
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def logout_view(request):
    request.auth.delete()  # delete the token to logout
    return Response({"detail": "Logged out successfully"}, status=200)







@swagger_auto_schema(
    method='post',
    operation_summary="Refresh Token",
    operation_description="Refresh the authentication token.",
    manual_parameters=[
        openapi.Parameter(
            'Authorization',
            openapi.IN_HEADER,
            description='Token authorization header: "Authorization: token <your_token>"',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    responses={
        200: openapi.Response(
            description="New token generated",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'token': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        ),
        401: openapi.Response(description="Unauthorized"),
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token_view(request):
    user = request.user
    # Delete old token
    request.auth.delete()
    # Create new token
    token = Token.objects.create(user=user)
    return Response({"token": token.key}, status=200)





