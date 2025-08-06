from apps.mark.models import Mark
from apps.mark.serializers.marks_serializer import MarkSerializer
from apps.student.models import Student
from apps.subject.models import Subject
from rest_framework import serializers
from django.db.models import Avg

from apps.report_card.models import ReportCard, Term
from apps.student.serializers.student_serializer import StudentField, StudentSerializer, StudentSerializerMinimal

class ReportCardSerializer(serializers.ModelSerializer):
    student = StudentSerializerMinimal()
    marks = MarkSerializer(many=True)
    class Meta:
        model = ReportCard
        fields = (
            "id",
            "student",
            "term",
            "year",
            "marks"
        )

class AddMarksReportCardSerializer(serializers.ModelSerializer):
    marks = serializers.ListField(child=serializers.JSONField())
    class Meta:
        model = ReportCard
        fields = (
            "marks",
        )
    
    def add_marks(self, instance):
        report_card = instance
        marks = self.data['marks']
        for mark in marks:
            subject_code = mark.pop('subject')
            subject = Subject.objects.get(code=subject_code)
            
            if report_card.marks.filter(subject=subject).exists():
                report_card.marks.filter(subject=subject).update(score=mark['score'])
            else:
                report_card.marks.create(subject=subject, score=mark['score'])

        report_card.refresh_from_db()
        return ReportCardSerializer(report_card).data

class ReportCardStudentYearSerializer(serializers.ModelSerializer):
    def student_by_year(self, student_id, year):
        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            raise serializers.ValidationError("Student does not exist")
        
        # Get all report cards for this student in this year
        report_cards = ReportCard.objects.filter(
            student=student,
            year=year
        ).prefetch_related('marks__subject')
        
        if not report_cards.exists():
            raise serializers.ValidationError("No report cards found for this year")
        
        # Serialize report cards
        report_cards_data = ReportCardSerializer(report_cards, many=True).data
        
        # Calculate subject averages
        subject_averages = Mark.objects.filter(
            report_card__student=student,
            report_card__year=year
        ).values('subject__name').annotate(avg_score=Avg('score'))
        
        # Calculate overall average
        overall_average = Mark.objects.filter(
            report_card__student=student,
            report_card__year=year
        ).aggregate(total_avg=Avg('score'))['total_avg']
        
        return {
            'student': StudentSerializer(student).data,
            'year': year,
            'report_cards': report_cards_data,
            'subject_averages': list(subject_averages),
            'overall_average': overall_average
        }

class ReportCardLoader(serializers.ModelSerializer):
    student = StudentField()

    def to_representation(self, instance):
        return ReportCardSerializer(instance, context=self.context).data
    
    class Meta:
        model = ReportCard
        fields = (
           "student",
           "term",
           "year",
        )

    def validate_term(self, value):
        if value == Term.BLANK:
            raise serializers.ValidationError("Term cannot be blank")
        return value
    
    def validate_year(self, value):
        if value < 2000:
            raise serializers.ValidationError("Year cannot be less than 2000")
        return value
    
    # def validate(self, data): # from model meta unique_together
    #     student = data['student']
    #     term = data['term']
    #     year = data['year']

    #     if ReportCard.objects.filter(
    #         student=student.id,
    #         term=term,
    #         year=year
    #     ).exists():
    #         raise serializers.ValidationError({
    #             "error": "Report card already exists"
    #         })
    #     return data