from django.db import models
from  django.contrib.auth.models import User
from  django.db.models.signals import  post_save
from  django.dispatch import  receiver
from django.contrib.auth.models import AbstractUser
from .choice import role ,target
from django.db import transaction
# Create your models here.

class Organization(models.Model):
    organization = models.CharField(max_length=255)

    def __str__(self):
        return self.organization


class Users(AbstractUser):
    is_user = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    # def __str__(self):
    #     return
class Admin(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE, primary_key=True, related_name='admin')
    organization = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.organization
#
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Admin.objects.create(user=instance)
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.admin.save()


class ScrummyUser(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE, primary_key=True, related_name='scrummyuser')

    role= models.CharField(max_length=100, choices=role, blank=True, null=True, default='DEV')
    org = models.ForeignKey(Admin, max_length=255, on_delete=models.CASCADE)
    # is_user = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


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


# @receiver(post_save, sender=Users)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         ScrummyUser.objects.create(user=instance)
#
#
# @receiver(post_save, sender=Users)
# def save_user_profile(sender, instance, **kwargs):
#     instance.scrummyuser.save()

#

class GoalStatus(models.Model):
    target = models.CharField(max_length=100, choices=target, default="Week")

    def __str__(self):
        return self.target



class ScrummyGoals(models.Model):
    user_name = models.ForeignKey(ScrummyUser, on_delete=models.CASCADE)
    #goal_status = models.ForeignKey(GoalStatus, on_delete=models.CASCADE)
    task = models.CharField(max_length=200)
    #task_target = models.CharField(max_length=30)
    target_name = models.ForeignKey(GoalStatus, on_delete=models.CASCADE, default=1, related_name="scrummygoals")



    def __str__(self):
        return self.task











