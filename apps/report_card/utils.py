from decimal import Decimal
import json

from apps.mark.models import Mark
from apps.report_card.models import ReportCard, ReportCardStatus
from django.db.models import Avg,F

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)

def calculate_report_card(report_card):
    student = report_card.student
    year = report_card.year
    # Calculate subject averages
    subject_averages = Mark.objects.filter(
        report_card__student=student,
        report_card__year=year
    ).values(subjectName=F('subject__name')).annotate(avg_score=Avg('score')) # 
    
    # Calculate overall average
    overall_average = Mark.objects.filter(
        report_card__student=student,
        report_card__year=year
    ).aggregate(total_avg=Avg('score')) # using db aggregate to get average

    subject_averages_json = json.dumps(list(subject_averages),cls=DecimalEncoder)

    # Update report card
    report_card.subject_averages = subject_averages_json
    report_card.overall_average = overall_average['total_avg']
    report_card.task_status = ReportCardStatus.COMPLETED
    report_card.save()

    # change other report_card of same person and year's task_status to not_started
    other_report_cards = ReportCard.objects.filter(
        student=student,
        year=year
    ).exclude(id=report_card.id).all()

    other_report_cards.update(
        task_status=ReportCardStatus.COMPLETED,
        subject_averages=subject_averages_json,
        overall_average=overall_average['total_avg']
        )

    return subject_averages_json,overall_average