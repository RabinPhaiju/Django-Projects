from django.db import models
from core.models import BaseModel
from apps.student.models import Student

class Term(models.TextChoices):
    Term1 = 'term1', 'Term 1'
    Term2 = 'term2', 'Term 2'
    Term3 = 'term3', 'Term 3'
    Term4 = 'term4', 'Term 4'
    BLANK = '', 'Blank'

class ReportCard(BaseModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='report_cards')
    term = models.CharField(
        max_length=10,
        choices=Term.choices,
        default=Term.BLANK,
        blank=True,
    )
    year = models.IntegerField()

    class Meta:
        unique_together = ('student', 'term', 'year')

    def __str__(self):
        return f"{self.student.name} - {self.term.value} {self.year}"