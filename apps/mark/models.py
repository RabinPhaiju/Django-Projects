from django.db import models
from apps.report_card.models import ReportCard
from apps.subject.models import Subject
from core.models import BaseModel

class Mark(BaseModel):
    report_card = models.ForeignKey(ReportCard, on_delete=models.CASCADE, related_name='marks')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.report_card} - {self.subject} - {self.score}"
