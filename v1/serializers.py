from rest_framework import serializers
from v1.models import (
    Content
)

class ContentCompleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ['id', 'completed']
