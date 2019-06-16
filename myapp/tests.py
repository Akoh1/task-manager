from django.test import TestCase
from .models import *
from  .forms import *

# Create your tests here.

class ModelTest(TestCase):
    def create_organization(self, organization="ehealth"):
        return Organization.objects.create(organization=organization)

    def test_create_organization(self):
        org = self.create_organization()
        self.assertTrue(isinstance(org, Organization))
        self.assertEqual(org.__str__(), org.organization)

    def test_valid_form(self):
        org = Organization.objects.create(organization="Andela")
        data = {'organization': org.organization}
        form = OrganizationForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        org = Organization.objects.create(organization="")
        data = {'organization': org.organization}
        form = OrganizationForm(data=data)
        self.assertTrue(form.is_valid())

    def test_valid_scrummy_form(self):
        org = User.objects.create(first_name="Akoh", last_name="Samuel",
                                  username="sasori", password="myuser123",
                                  email="akohsamuel018@gmail.com",
                                  role="DEV", org=1)
        data = {'first_name': org.first_name, 'last_name':org.last_name,
                'username': org.username, 'password1':org.password1,
                'password2':org.password2, 'email':org.email, 'role':org.role, 'org':org.org}
        form = ScrummySignUpForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_scrummy_form(self):
        org = User.objects.create(first_name="Akoh", last_name="Samuel",
                                  username="sasori", password1="",
                                  email="",
                                  role="DEV", org=1)
        data = {'first_name': org.first_name, 'last_name':org.last_name,
                'username': org.username, 'password1':org.password1,
                'password2':org.password2, 'email':org.email, 'role':org.role, 'org':org.org}
        form = ScrummySignUpForm(data=data)
        self.assertTrue(form.is_valid())