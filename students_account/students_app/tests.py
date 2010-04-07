from datetime import datetime
from django.db.models import Count
from django.test import TestCase, Client
from students_app.models import Grup, Student

class SimpleTest(TestCase):

    def setUp(self):
        self.valid_user = {'username':'1', 'password':'1', 'email':'1@1.com'}
        self.invalid_user = {'username':'345', 'password':'1', 'email':'1@2.com'}

    def test_client_username_login(self):
        """ test login using valid username"""
        is_logged_in = self.client.login(username=self.valid_user['username'],
                                         password=self.valid_user['password'])
        self.assertEqual(is_logged_in, True)
        response = self.client.post('/groups/')
        self.assertEqual(response.status_code, 200)

    def test_client_email_login(self):
        """ test login using valid email"""
        is_logged_in = self.client.login(username=self.valid_user['email'],
                                         password=self.valid_user['password'])
        self.assertEqual(is_logged_in, True)
        response = self.client.post('/groups/')
        self.assertEqual(response.status_code, 200)

    def test_client_invalid_credentials_login(self):
        """ test login using invalid credentials"""
        is_logged_in = self.client.login(username=self.invalid_user['username'],
                                         password=self.invalid_user['password'])
        self.assertEqual(is_logged_in, False)
        response = self.client.post('/groups/')
        self.assertNotEqual(response.status_code, 200)

    def test_add_group(self):
        """ test adding a group"""
        self._add_group()

    def test_add_student(self):
        """ test successful adding a group and a student into it"""
        new_group = self._add_group()
        if new_group:
            test_student = {'surname': 'test_surname',
                              'name':'test_name',
                              'patronymic':'test_patronymic',
                              'birth_date':'2010-01-01',
                              'student_card':'124df',
                              'grup':new_group.pk}
            url = '/students/%s' % new_group.name

            self.assertEqual(self.client.get(url).status_code, 200)
            self.client.post(url, test_student)
            new_student = Student.objects.get(name='test_surname', name='test_name')
            self.assertNotEqual(new_student.pk, None)
            self.assertEqual(new_student.surname, test_student['surname'])
            self.assertEqual(new_student.name, test_student['name'])
            self.assertEqual(new_student.patronymic, test_student['patronymic'])
            self.assertEqual(new_student.birth_date.strftime('%Y-%m-%d'),
                             test_student['birth_date'])
            self.assertEqual(new_student.student_card, test_student['student_card'])

            students_amount = Student.objects.filter(grup=new_group).count()
            self.assertEqual(students_amount, 1)

    def test_add_invalid_student(self):
        """ test adding a group and a student containing invalid data into it"""
        new_group = self._add_group()
        if new_group:
            test_student = {'surname': 'test_surname',
                            'name':'test_name',
                            'patronymic':'test_patronymic',
                            'birth_date':'inv_date',
                            'student_card':'124df',
                            'grup':new_group.pk}
            url = '/students/%s' % new_group.name
            self.assertEqual(self.client.get(url).status_code, 200)
            response = self.client.post(url, test_student)

            self.assertRaises(Student.DoesNotExist,
                              Student.objects.get,
                              name='test_surname', name='test_name')
            self.assertFormError(response, 'form', 'birth_date', 'Enter a valid date.')
            students_amount = Student.objects.filter(grup=new_group).count()
            self.assertEqual(students_amount, 0)

    def _add_group(self):
        is_logged_in = self.client.login(username=self.valid_user['username'],
                                         password=self.valid_user['password'])
        if is_logged_in:
            url = '/groups/'
            response = self.client.post(url,
                                        {'name': 'test_group',
                                         'captain': '', 'pk':''})

            new_group = Grup.objects.get(name='test_group')
            self.assertNotEqual(new_group.pk, None)
            self.assertEqual(new_group.name, 'test_group')
            self.assertEqual(new_group.captain, None)
            students_amount = Student.objects.filter(grup=new_group).count()
            self.assertEqual(students_amount, 0)
            return new_group
        return None
