from decimal import Decimal
import json
from celery import shared_task

from apps.mark.models import Mark
from apps.report_card.models import ReportCard, ReportCardStatus
from django.db.models import Avg,F

from apps.report_card.utils import calculate_report_card



@shared_task(queue="report_tasks")
def calculate_report_card_aggregate(report_card_id):
    report_card = ReportCard.objects.select_related('student').get(id=report_card_id)

    if report_card:
        calculate_report_card(report_card)

    return True