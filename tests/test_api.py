from django.urls import reverse
from core.models.user import User
from rest_framework.test import APITestCase
from rest_framework import status
from apps.student.models import Student
from apps.subject.models import Subject
from apps.report_card.models import ReportCard
from apps.mark.models import Mark

from rest_framework_simplejwt.tokens import RefreshToken

class AuthenticatedAPITest(APITestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='admin',
            password='admin'
        )
        self.group = self.user.groups.create(name='system_admin')
        self.user.groups.add(self.group)
        
        # Get JWT tokens
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        
        # Set credentials
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        self.student_data = {
            'name': 'John Doe',
            'email': 'jane@example.com',
            'date_of_birth': '2000-01-01'
        }
        
        self.list_url = '/api/v1/students/'

    def test_create_student_authenticated(self):
        """Test creating a student with authentication"""
        response = self.client.post(self.list_url, self.student_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Student.objects.count(), 1)
        self.assertEqual(Student.objects.get().name, 'John Doe')

    def test_create_student_unauthenticated(self):
        """Test that unauthenticated requests are rejected"""
        # Remove authentication
        self.client.credentials()
        
        response = self.client.post(self.list_url, self.student_data, format='json')
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])


class ReportCardAPITest(APITestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='admin1',
            password='admin1'
        )
        self.group = self.user.groups.create(name='system_admin')
        self.user.groups.add(self.group)
        
        # Get JWT tokens
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        
        # Set credentials
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        self.student = Student.objects.create(
            name="John Doe",
            email="john@example.com",
            date_of_birth="2000-01-01"
        )
        
        self.subject = Subject.objects.create(
            name="Mathematics",
            code="MATH101"
        )

        self.report_card_data = {
            'student': self.student.id,
            'term': 'term1',
            'year': 2024
        }
        
        # Use actual URLs
        self.list_url = '/api/v1/report-cards/'
        self.year_url = f'/api/v1/report-cards/student/{self.student.id}/year/2024/'
        self.marks_url = lambda rc_id: f'/api/v1/report-cards/{rc_id}/add-marks/'

    def test_create_report_card(self):
        """Test creating a report card"""
        response = self.client.post(self.list_url, self.report_card_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check database
        self.assertEqual(ReportCard.objects.count(), 1)

    def test_get_student_year_report_cards(self):
        """Test getting all report cards for student in a year"""
        # Create test data
        ReportCard.objects.create(student=self.student, term="term1", year=2024)
        ReportCard.objects.create(student=self.student, term="term2", year=2024)
        
        response = self.client.get(self.year_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        response_data = response.json()
        self.assertIn('report_cards', response_data)
        self.assertIn('subject_averages', response_data)
        self.assertIn('overall_average', response_data)