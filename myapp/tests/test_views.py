from django.test import TestCase, Client
from django.urls import reverse
from myapp.models import *
import json

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.index = reverse('myapp:index')
        self.home = reverse('myapp:home')
        # self.move = reverse('myapp:move_goal', args=[1])

    def test_index_GET(self):
        response = self.client.get(self.index)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'myapp/index.html')

    def test_home_GET(self):
        response = self.client.get(self.home)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'myapp/home.html')

    # def test_move_GET(self):
    #     response = self.client.get(self.move)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'myapp/move_task.html')

