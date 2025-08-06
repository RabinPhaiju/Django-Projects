from report_card_system.utils import is_int_parsable
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from apps.student.models import Student
from django.db.models import Q

@extend_schema_field(serializers.CharField())
class StudentField(serializers.Field):
    def to_representation(self, value):
        return value.id

    def to_internal_value(self, data):
        try:
            if is_int_parsable(data):
                return Student.objects.get(id=int(data))
            else:
                return Student.objects.get(Q(name__iexact=data))
        except Student.DoesNotExist:
            raise serializers.ValidationError("Student does not exist.")

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
