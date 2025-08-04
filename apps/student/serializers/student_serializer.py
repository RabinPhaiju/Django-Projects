from rest_framework import serializers

from apps.student.models import Student


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = (
            "id",
            "name",
            "email",
            "date_of_birth",
        )

class StudentSerializerMinimal(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = (
            "id",
            "name",
        )

class StudentLoader(serializers.ModelSerializer):
    def to_representation(self, instance):
        return StudentSerializer(instance, context=self.context).data
    
    class Meta:
        model = Student
        fields = (
           "name",
           "email",
           "date_of_birth",
        )
