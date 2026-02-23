# students/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from datetime import date, timedelta
from .models import Student, StudentDocument
from .forms import StudentForm

User = get_user_model()


class StudentModelTest(TestCase):
    """Test cases for Student model"""
    
    def setUp(self):
        """Set up test data"""
        self.student = Student.objects.create(
            first_name='Ali',
            last_name='Valiyev',
            email='ali@example.com',
            phone_number='+998901234567',
            date_of_birth=date(2000, 1, 1),
            gender='M',
            address='Tashkent, Yunusobod',
            city='Tashkent',
            status='active'
        )
    
    def test_student_creation(self):
        """Test student is created correctly"""
        self.assertEqual(self.student.first_name, 'Ali')
        self.assertEqual(self.student.last_name, 'Valiyev')
        self.assertTrue(self.student.student_id.startswith('STD'))
    
    def test_student_str(self):
        """Test string representation"""
        expected = f"Ali Valiyev ({self.student.student_id})"
        self.assertEqual(str(self.student), expected)
    
    def test_get_full_name(self):
        """Test get_full_name method"""
        self.assertEqual(self.student.get_full_name(), 'Ali Valiyev')
    
    def test_get_age(self):
        """Test age calculation"""
        today = date.today()
        expected_age = today.year - 2000
        if (today.month, today.day) < (1, 1):
            expected_age -= 1
        self.assertEqual(self.student.get_age(), expected_age)
    
    def test_student_id_auto_generation(self):
        """Test automatic student ID generation"""
        student2 = Student.objects.create(
            first_name='Vali',
            last_name='Aliyev',
            email='vali@example.com',
            phone_number='+998901234568',
            date_of_birth=date(2001, 1, 1),
            gender='M',
            address='Tashkent',
            city='Tashkent'
        )
        self.assertTrue(student2.student_id)
        self.assertNotEqual(student2.student_id, self.student.student_id)
    
    def test_activate_deactivate(self):
        """Test activate and deactivate methods"""
        self.student.deactivate()
        self.assertEqual(self.student.status, 'inactive')
        
        self.student.activate()
        self.assertEqual(self.student.status, 'active')
    
    def test_graduate(self):
        """Test graduate method"""
        self.student.graduate()
        self.assertEqual(self.student.status, 'graduated')
        self.assertIsNotNone(self.student.graduation_date)


class StudentFormTest(TestCase):
    """Test cases for StudentForm"""
    
    def test_valid_form(self):
        """Test form with valid data"""
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'phone_number': '+998901234567',
            'date_of_birth': '2000-01-01',
            'gender': 'M',
            'address': 'Test Address',
            'city': 'Tashkent',
            'status': 'active',
        }
        form = StudentForm(data=data)
        self.assertTrue(form.is_valid())
    
    def test_invalid_email(self):
        """Test form with invalid email"""
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'invalid-email',
            'phone_number': '+998901234567',
            'date_of_birth': '2000-01-01',
            'gender': 'M',
            'address': 'Test',
            'city': 'Tashkent',
        }
        form = StudentForm(data=data)
        self.assertFalse(form.is_valid())
    
    def test_invalid_phone(self):
        """Test form with invalid phone"""
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'phone_number': '123',
            'date_of_birth': '2000-01-01',
            'gender': 'M',
            'address': 'Test',
            'city': 'Tashkent',
        }
        form = StudentForm(data=data)
        self.assertFalse(form.is_valid())
    
    def test_future_birth_date(self):
        """Test form with future birth date"""
        future_date = date.today() + timedelta(days=1)
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'phone_number': '+998901234567',
            'date_of_birth': future_date,
            'gender': 'M',
            'address': 'Test',
            'city': 'Tashkent',
        }
        form = StudentForm(data=data)
        self.assertFalse(form.is_valid())


class StudentViewTest(TestCase):
    """Test cases for Student views"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        self.student = Student.objects.create(
            first_name='Ali',
            last_name='Valiyev',
            email='ali@example.com',
            phone_number='+998901234567',
            date_of_birth=date(2000, 1, 1),
            gender='M',
            address='Tashkent',
            city='Tashkent'
        )
    
    def test_student_list_view(self):
        """Test student list view"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('students:student_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ali')
    
    def test_student_detail_view(self):
        """Test student detail view"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('students:student_detail', kwargs={'pk': self.student.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ali Valiyev')
    
    def test_student_create_view_get(self):
        """Test student create view GET request"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('students:student_create'))
        self.assertEqual(response.status_code, 200)
    
    def test_student_search(self):
        """Test student search functionality"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('students:student_list') + '?search=Ali'
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ali')
    
    def test_unauthorized_access(self):
        """Test unauthorized access redirects to login"""
        response = self.client.get(reverse('students:student_list'))
        self.assertEqual(response.status_code, 302)  # Redirect to login


class StudentDocumentTest(TestCase):
    """Test cases for StudentDocument model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        self.student = Student.objects.create(
            first_name='Ali',
            last_name='Valiyev',
            email='ali@example.com',
            phone_number='+998901234567',
            date_of_birth=date(2000, 1, 1),
            gender='M',
            address='Tashkent',
            city='Tashkent'
        )
    
    def test_document_creation(self):
        """Test document creation"""
        doc = StudentDocument.objects.create(
            student=self.student,
            document_type='passport',
            title='Pasport',
            uploaded_by=self.user
        )
        self.assertEqual(doc.student, self.student)
        self.assertEqual(doc.document_type, 'passport')
    
    def test_document_str(self):
        """Test document string representation"""
        doc = StudentDocument.objects.create(
            student=self.student,
            document_type='passport',
            title='Pasport',
            uploaded_by=self.user
        )
        expected = f"Ali Valiyev ({self.student.student_id}) - Pasport"
        self.assertEqual(str(doc), expected)