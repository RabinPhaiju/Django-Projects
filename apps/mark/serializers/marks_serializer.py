from apps.subject.serializers.subject_serializer import SubjectSerializer
from rest_framework import serializers

from apps.mark.models import Mark

class MarkSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer(read_only=True)
    class Meta:
        model = Mark
        fields = (
            "id",
            "score",
            "subject",
        )

class MarkLoader(serializers.ModelSerializer):
    def to_representation(self, instance):
        return MarkSerializer(instance, context=self.context).data
    
    class Meta:
        model = Mark
        fields = (
           "score",
           "subject",
        )
