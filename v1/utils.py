from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from v1.models import (
    Content
)
from students.models import (
    TopicProgress
)

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



def update_topic_progress(student, topic):
    contents = Content.objects.filter(topic=topic)
    total = contents.count()
    if total == 0:
        percentage = 0
    else:
        completed_count = contents.filter(completed=True).count()
        percentage = (completed_count / total) * 100

    progress, created = TopicProgress.objects.get_or_create(
        student=student,
        topic=topic,
        defaults={
            'completion_percentage': percentage,
            'is_completed': percentage == 100
        }
    )
    if not created:
        progress.completion_percentage = percentage
        progress.is_completed = percentage == 100
        progress.save()
