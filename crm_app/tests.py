from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Record
from .forms import AddRecordForm

class RecordModelTests(TestCase):
    def test_str_representation(self):
        record = Record(first_name="John", last_name="Doe")
        self.assertEqual(str(record), "John Doe")

class ViewsTests(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(username='testuser', password='testpassword')
        self.test_record = Record.objects.create(first_name='John', last_name='Doe', phone='1234567890',
                                                 email='john.doe@example.com', city='New York', state='NY')

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_register_user_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_customer_record_view_authenticated_user(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('record', args=[self.test_record.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'record.html')

    def test_customer_record_view_unauthenticated_user(self):
        response = self.client.get(reverse('record', args=[self.test_record.id]))
        self.assertRedirects(response, '/') 


class AddRecordFormTests(TestCase):
    def test_valid_form(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'phone': '1234567890',
            'email': 'john.doe@example.com',
            'city': 'New York',
            'state': 'NY',
        }
        form = AddRecordForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_blank_form(self):
        form = AddRecordForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 6)

