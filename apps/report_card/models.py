from django.db import models
from core.models import BaseModel
from apps.student.models import Student

class Term(models.TextChoices):
    Term1 = 'term1', 'Term 1'
    Term2 = 'term2', 'Term 2'
    Term3 = 'term3', 'Term 3'
    Term4 = 'term4', 'Term 4'
    BLANK = '', 'Blank'

class ReportCardStatus(models.TextChoices):
    COMPLETED = 'COMPLETED', 'Completed'
    IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
    NOT_STARTED = 'NOT_STARTED', 'Not Started'

class ReportCard(BaseModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='report_cards')
    term = models.CharField(
        max_length=10,
        choices=Term.choices,
        default=Term.BLANK,
        blank=True,
    )
    year = models.IntegerField()

    subject_averages = models.JSONField(default=dict, blank=True)
    overall_average = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.0,
        blank=True,
    )
    task_status = models.CharField(
        max_length=20,
        choices=ReportCardStatus.choices,
        default=ReportCardStatus.NOT_STARTED,
        blank=True,
    )
    class Meta:
        unique_together = ('student', 'term', 'year')
        indexes = [
            models.Index(fields=['student', 'year']),
            models.Index(fields=['term']),
        ]

    def __str__(self):
        return f"{self.student.name} - {self.term} {self.year}"