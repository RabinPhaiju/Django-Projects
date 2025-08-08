import json
from apps.mark.models import Mark
from apps.mark.serializers.marks_serializer import MarkSerializer
from apps.report_card.tasks import calculate_report_card_aggregate
from apps.report_card.utils import calculate_report_card
from apps.student.models import Student
from apps.subject.models import Subject
from rest_framework import serializers
from django.db.models import Avg,F

from apps.report_card.models import ReportCard, ReportCardStatus, Term
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
        marks_data = self.data['marks']

        subject_codes = [mark['subject'] for mark in marks_data]
        subjects = Subject.objects.in_bulk(subject_codes, field_name='code') # get all subjects at once.

        marks_to_create = []
        marks_to_update = []
        for mark_data in marks_data:
            subject_code = mark_data.pop('subject')
            score = mark_data['score']
            if subject_code not in subjects:
                raise serializers.ValidationError(f"Subject with code {subject_code} does not exist")
            
            subject = subjects[subject_code]

            # Check if mark already exists
            existing_marks = report_card.marks.filter(subject=subject).first()
            if existing_marks:
                existing_marks.score = score
                marks_to_update.append(existing_marks)
            else:
                mark = Mark(report_card=report_card, subject=subject, score=score)
                marks_to_create.append(mark)
            
        if marks_to_create:
            # Bulk create to reduce number of queries on save
            Mark.objects.bulk_create(marks_to_create)
        if marks_to_update:
            Mark.objects.bulk_update(marks_to_update, ['score'])

        # trigger celery task for report_card_aggregate
        report_card.task_status = ReportCardStatus.IN_PROGRESS
        calculate_report_card_aggregate.delay(report_card.id)
    
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
        ).prefetch_related('marks__subject') # Eager load marks
        
        if not report_cards.exists():
            raise serializers.ValidationError("No report cards found for this year")
        
        # Serialize report cards
        report_cards_data = ReportCardSerializer(report_cards, many=True).data

        # check if report aggregate is already calculated
        report_card = ReportCard.objects.filter(
            student=student,
            year=year,
            subject_averages__isnull=False,
            overall_average__gt=0.0,
            task_status=ReportCardStatus.COMPLETED
        ).first()
        if report_card:
            return {
                'student': StudentSerializer(student).data,
                'year': year,
                'report_cards': report_cards_data,
                'subject_averages': json.loads(report_card.subject_averages),
                'overall_average': report_card.overall_average,
            }
        
        # Fallback incase report aggregate is not calculated
        report_card = ReportCard.objects.select_related('student').filter(student=student,year=year).first()
        sub_avg,overall_avg = calculate_report_card(report_card)
        return {
            'student': StudentSerializer(student).data,
            'year': year,
            'report_cards': report_cards_data,
            'subject_averages': sub_avg,
            'overall_average': overall_avg,
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