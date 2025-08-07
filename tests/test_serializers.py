from django.test import TestCase
from rest_framework.test import APITestCase
from apps.student.models import Student
from apps.subject.models import Subject
from apps.report_card.models import ReportCard
from apps.mark.models import Mark
from apps.student.serializers.student_serializer import StudentSerializer
from apps.subject.serializers.subject_serializer import SubjectSerializer
from apps.report_card.serializers.report_card_serializer import ReportCardSerializer
from apps.mark.serializers.marks_serializer import MarkSerializer

class StudentSerializerTest(APITestCase):
    def setUp(self):
        self.student_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'date_of_birth': '2000-01-01'
        }

    def test_student_serializer_valid_data(self):
        """Test student serializer with valid data"""
        serializer = StudentSerializer(data=self.student_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['name'], 'John Doe')

    def test_student_serializer_invalid_email(self):
        """Test student serializer with invalid email"""
        invalid_data = self.student_data.copy()
        invalid_data['email'] = 'invalid-email'
        
        serializer = StudentSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)

class SubjectSerializerTest(APITestCase):
    def setUp(self):
        self.subject_data = {
            'name': 'Mathematics',
            'code': 'MATH101'
        }

    def test_subject_serializer_valid_data(self):
        """Test subject serializer with valid data"""
        serializer = SubjectSerializer(data=self.subject_data)
        self.assertTrue(serializer.is_valid())

class ReportCardSerializerTest(APITestCase):
    def setUp(self):
        self.student = Student.objects.create(
            name="John Doe",
            email="john@example.com",
            date_of_birth="2000-01-01"
        )

        self.subject = Subject.objects.create(
            name="Math",
            code="math"
        )
        
        self.report_card_data =  {
        'student': {
            'name': self.student.name,
            'email': self.student.email,
            'date_of_birth': self.student.date_of_birth
        },
        'term': 'term1',
        'year': 2024,
        'marks': [
            {
                'subject': {
                    'id': self.subject.id,
                    'name': self.subject.name,
                    'code': self.subject.code
                },
                'score': 85.5
            }
        ]
    }

    def test_report_card_serializer_create(self):
        """Test report card serializer create"""
        serializer = ReportCardSerializer(data=self.report_card_data)
        serializer.is_valid()
        self.assertTrue(serializer.is_valid())
        
    def test_report_card_serializer_read(self):
        """Test report card serializer read with nested data"""
        report_card = ReportCard.objects.create(
            student=self.student,
            term="term1",
            year=2024
        )
        
        # Add a mark
        Mark.objects.create(
            report_card=report_card,
            subject=self.subject,
            score=85.5
        )
        
        # Refresh with related data
        report_card = ReportCard.objects.select_related('student').prefetch_related('marks__subject').get(id=report_card.id)
        serializer = ReportCardSerializer(report_card)
        
        data = serializer.data
        self.assertIn('student', data)
        self.assertIn('marks', data)
        self.assertEqual(len(data['marks']), 1)
        self.assertEqual(data['marks'][0]['score'], '85.50')