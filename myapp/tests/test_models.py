from django.test import TestCase
from myapp.models import *
from  myapp.forms import *

# Create your tests here.

class ModelTest(TestCase):
    def setUp(self):
        self.user= Users.objects.create(first_name='Test', last_name='test1',
                                       email='test@gmail.com', username='mytest',
                                       password='password1')
        self.scrummyuser = Users.objects.create(first_name='Scrummy', last_name='User',
                                         email='scrummy@gmail.com', username='scrummy',
                                         password='password1')
        self.status = GoalStatus.objects.create(target='Week')

    def create_admin_model(self):
        admin = Admin.objects.create(user=self.user, organization='erpSOFTapp')
        return admin

    def test_admin_model(self):
        admin = self.create_admin_model()
        self.assertTrue(isinstance(admin, Admin))
        self.assertEqual(admin.organization, admin.__str__())

    def create_user_model(self):
        admin = self.create_admin_model()
        scrummy = ScrummyUser.objects.create(user=self.scrummyuser, role='DEV', org=admin)
        return scrummy

    def test_user_model(self):
        scrummy = self.create_user_model()
        self.assertTrue(isinstance(scrummy, ScrummyUser))
        self.assertEqual(scrummy.user.username, scrummy.__str__())

    def create_goals_model(self):
        user = self.create_user_model()
        goal = ScrummyGoals.objects.create(user_name=user, task='Test Task', target_name=self.status)
        return goal

    def test_goal_model(self):
        goals = self.create_goals_model()
        self.assertTrue(isinstance(goals, ScrummyGoals))
        self.assertEqual(goals.task, goals.__str__())
