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
        adm = Admin.objects.get(user_id=1)
        org = Users.objects.create(first_name="Akoh", last_name="Samuel",
                                  username="sasori", password="myuser123",
                                  email="akohsamuel018@gmail.com")
        scrum = ScrummyUser.objects.create(user=org, role="DEV", org=adm.id)
        data = {'first_name': org.first_name, 'last_name':org.last_name,
                'username': org.username, 'password':org.password,
             	'email':org.email, 'role': scrum.role, 'org':scrum.org}
        form = UserForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_scrummy_form(self):
        org = Users.objects.create(first_name="Akoh", last_name="Samuel",
                                  username="sasori", password="",
                                  email="")
        data = {'first_name': org.first_name, 'last_name':org.last_name,
                'username': org.username, 'password':org.password,
                'email':org.email}
        form = UserForm(data=data)
        self.assertTrue(form.is_valid())
