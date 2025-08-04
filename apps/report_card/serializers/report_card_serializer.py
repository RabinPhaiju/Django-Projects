from rest_framework import serializers

from apps.report_card.models import ReportCard
from apps.student.serializers.student_serializer import StudentSerializerMinimal

class ReportCardSerializer(serializers.ModelSerializer):
    student = StudentSerializerMinimal()
    class Meta:
        model = ReportCard
        fields = (
            "id",
            "student",
            "term",
            "year",
        )

class ReportCardLoader(serializers.ModelSerializer):
    def to_representation(self, instance):
        return ReportCardSerializer(instance, context=self.context).data
    
    class Meta:
        model = ReportCard
        fields = (
           "student",
           "term",
           "year",
        )
