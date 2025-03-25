from rest_framework import serializers

from tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = (
            "id",
            "title",
            "description",
            "status",
            "user",
            "created_at",
            "updated_at",
        )


class TaskLoaderSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        return TaskSerializer(instance, context=self.context).data
    
    class Meta:
        model = Task
        fields = (
            "title",
            "description",
            "status",
        )

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
    
    
