# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.report_card.tasks import calculate_report_card_aggregate
from .models import Mark

@receiver(post_save, sender=Mark)
def trigger_aggregation_on_mark_change(sender, instance, **kwargs):
    calculate_report_card_aggregate.delay(instance.report_card.id)