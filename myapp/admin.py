from django.contrib import admin
from .models import ScrummyUser, ScrummyGoals, GoalStatus
from  django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
# Register your models here.

admin.site.register(ScrummyUser)
admin.site.register(ScrummyGoals)
admin.site.register(GoalStatus)
#admin.site.register(UserAdmin)