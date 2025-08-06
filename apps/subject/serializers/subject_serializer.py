from rest_framework import serializers

from apps.subject.models import Subject

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = (
            "id",
            "name",
            "code",
        )

class SubjectLoader(serializers.ModelSerializer):
    def to_representation(self, instance):
        return SubjectSerializer(instance, context=self.context).data
    
    class Meta:
        model = Subject
        fields = (
           "name",
           "code",
        )
