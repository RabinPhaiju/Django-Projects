from django.test import TestCase
from apps.student.models import Student
from apps.subject.models import Subject
from apps.report_card.models import ReportCard
from apps.mark.models import Mark

class StudentModelTest(TestCase):
    def setUp(self):
        self.student = Student.objects.create(
            name="John Doe",
            email="john@example.com",
            date_of_birth="2000-01-01"
        )

    def test_student_creation(self):
        """Test student is created correctly"""
        self.assertEqual(self.student.name, "John Doe")
        self.assertEqual(self.student.email, "john@example.com")

    def test_unique_email_constraint(self):
        """Test email must be unique"""
        with self.assertRaises(Exception):
            Student.objects.create(
                name="Jane Doe",
                email="john@example.com",  # Duplicate email
                date_of_birth="2000-01-01"
            )

class SubjectModelTest(TestCase):
    def setUp(self):
        self.subject = Subject.objects.create(
            name="Mathematics",
            code="MATH101"
        )

    def test_subject_creation(self):
        """Test subject is created correctly"""
        self.assertEqual(self.subject.name, "Mathematics")
        self.assertEqual(self.subject.code, "MATH101")

    def test_unique_code_constraint(self):
        """Test subject code must be unique"""
        with self.assertRaises(Exception):
            Subject.objects.create(
                name="Math II",
                code="MATH101"  # Duplicate code
            )

class ReportCardModelTest(TestCase):
    def setUp(self):
        self.student = Student.objects.create(
            name="John Doe",
            email="john@example.com",
            date_of_birth="2000-01-01"
        )
        
        self.subject = Subject.objects.create(
            name="Mathematics",
            code="MATH101"
        )

    def test_report_card_creation(self):
        """Test report card is created correctly"""
        report_card = ReportCard.objects.create(
            student=self.student,
            term="Term1",
            year=2024
        )
        
        self.assertEqual(str(report_card), "John Doe - Term1 2024")
        self.assertEqual(report_card.student, self.student)

    def test_unique_constraint(self):
        """Test cannot have duplicate report cards"""
        ReportCard.objects.create(
            student=self.student,
            term="Term1",
            year=2024
        )
        
        with self.assertRaises(Exception):
            ReportCard.objects.create(
                student=self.student,
                term="Term1",
                year=2024  # Same student, term, year
            )

class MarkModelTest(TestCase):
    def setUp(self):
        self.student = Student.objects.create(
            name="John Doe",
            email="john@example.com",
            date_of_birth="2000-01-01"
        )
        
        self.subject = Subject.objects.create(
            name="Mathematics",
            code="MATH101"
        )
        
        self.report_card = ReportCard.objects.create(
            student=self.student,
            term="Term1",
            year=2024
        )

    def test_mark_creation(self):
        """Test mark is created correctly"""
        mark = Mark.objects.create(
            report_card=self.report_card,
            subject=self.subject,
            score=85.5
        )
        
        self.assertEqual(mark.score, 85.5)
        self.assertEqual(mark.report_card, self.report_card)
        self.assertEqual(mark.subject, self.subject)
        
        expected_str = f"{self.report_card} - {self.subject} - 85.5"
        self.assertEqual(str(mark), expected_str)