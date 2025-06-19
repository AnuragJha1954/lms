from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status


def get_user_from_token(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.lower().startswith('token '):
        return None, Response({"detail": "Authorization header missing or invalid"}, status=status.HTTP_401_UNAUTHORIZED)
    
    token_key = auth_header.split(' ', 1)[1]
    try:
        token = Token.objects.get(key=token_key)
        return token.user, None
    except Token.DoesNotExist:
        return None, Response({"detail": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
