from django.db import models
from  django.contrib.auth.models import User
from  django.db.models.signals import  post_save
from  django.dispatch import  receiver

# Create your models here.

role = (('AD', 'Admin'),
        ('OW', 'Owner'),
        ('QT','Quality Analyst')
         ,('DV','DEVELOPER'))

target = (('Week', 'Weekly target'),
          ('Day', 'Daily target'),
          ('Verify', 'Verify'),
          ('Done', 'Done'))

class ScrummyUser(User):

    class Meta:
        proxy = True

    def __str__(self):
        return self.username

    def get_day(self):
        var = GoalStatus.objects.get(id=2)
        return self.scrummygoals_set.filter(target_name_id=var)

    def get_week(self):
        var = GoalStatus.objects.get(id=1)
        return self.scrummygoals_set.filter(target_name_id=var)
    def get_verify(self):
        var = GoalStatus.objects.get(id=3)
        return self.scrummygoals_set.filter(target_name_id=var)
    def get_done(self):
        var = GoalStatus.objects.get(id=4)
        return self.scrummygoals_set.filter(target_name_id=var)






class GoalStatus(models.Model):
    target = models.CharField(max_length=100, choices=target)

    def __str__(self):
        return self.target



class ScrummyGoals(models.Model):
    user_name = models.ForeignKey(ScrummyUser, on_delete=models.CASCADE)
    #goal_status = models.ForeignKey(GoalStatus, on_delete=models.CASCADE)
    task = models.CharField(max_length=200)
    #task_target = models.CharField(max_length=30)
    target_name = models.ForeignKey(GoalStatus, on_delete=models.CASCADE, default=1)



    def __str__(self):
        return self.task











