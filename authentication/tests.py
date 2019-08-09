from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages

# Create your tests here.
class AuthenticationTestCase(TestCase):
    def test_index_page(self):
        client = Client()
        response = client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_index_page_after_login(self):
        client = Client()
        client.post(reverse('signup'), {"first_name": "john",
                                                    "last_name": "doe",
                                                    "user_name": "jdoe", 
                                                    "email": "test@gmail.com",
                                                     "password": "Test1234@", 
                                                     "confirm_password": "Test1234@"})
        client.post(reverse('login'), {
                "username": "jdoe", "password": "Test1234@"})
        response = client.get(reverse('index'))
        self.assertEqual(response.status_code, 302)    

    def test_login_page(self):
        client = Client()
        response = client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_signup_page(self):
        client = Client()
        response = client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)    

    def test_sign_up_pass(self):
        client = Client()
        response = client.post(reverse('signup'), {"first_name": "john",
                                                    "last_name": "doe",
                                                    "user_name": "jdoe", 
                                                    "email": "test@gmail.com",
                                                     "password": "Test1234@", 
                                                     "confirm_password": "Test1234@"})
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         'You have been successfully logged in.')
        self.assertEqual(response.status_code, 302)

    def test_sign_up_fail(self):
        client = Client()
        response = client.post(reverse('signup'), {"first_name": "john",
                                                    "last_name": "doe",
                                                    "user_name": "jdoe",
                                                    "email": "test@gmail.com",
                                                    "password": "Test1234@233",
                                                    "confirm_password": "Test1234@"})
        self.assertEqual(response.status_code, 200)

    def test_login_pass(self):
        client = Client()
        client.post(reverse('signup'), {"first_name": "john",
                                                    "last_name": "doe",
                                                    "user_name": "jdoe", 
                                                    "email": "test@gmail.com",
                                                     "password": "Test1234@", 
                                                     "confirm_password": "Test1234@"})
        response = client.post(reverse('login'), {
                               "username": "jdoe", "password": "Test1234@"})
        self.assertEqual(response.status_code, 302)

    def test_login_fail(self):
        client = Client()
        response = client.post(reverse('login'), {"user_name": "jdoe","password": "Test1234@"})
        self.assertEqual(response.status_code, 200)

    def test_logout_pass(self):
        client = Client()
        client.post(reverse('signup'), {"first_name": "john",
                                         "last_name": "doe",
                                         "user_name": "jdoe",
                                         "email": "test@gmail.com",
                                         "password": "Test1234@",
                                                     "confirm_password": "Test1234@",
                                                     "customer": True})
        response = client.post(reverse('login'), {
                               "username": "jdoe", "password": "Test1234@"})
        response = client.get(reverse('signout'))
        self.assertEqual(response.status_code, 302)    


