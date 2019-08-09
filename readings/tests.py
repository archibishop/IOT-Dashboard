from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch, MagicMock, PropertyMock
import requests

# Create your tests here.
class ReadingTestCase(TestCase):
    @patch.object(requests, 'get')
    def test_home_page(self , api_request_get):
        data = {'feeds':[{'field1': '20.12','field2': '85.54', 'field3': '946.75'}]}
        r = requests.Response()
        r.status_code = 200
        def json_func():
            return data
        r.json = json_func                
        client = Client()
        api_request_get.return_value = r
        response = client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
