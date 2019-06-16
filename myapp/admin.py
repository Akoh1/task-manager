from django.contrib import admin
from .models import ScrummyUser, ScrummyGoals, GoalStatus, Organization, Users, Admin
# from  django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
# Register your models here.


@admin.register(ScrummyUser)
class ScrummyUserAdmin(admin.ModelAdmin):
    list_display = [ 'user_id', 'user', 'role', 'org']
admin.site.register(ScrummyGoals)
# admin.site.register(GoalStatus)
@admin.register(GoalStatus)
class GoalStatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'target']
# admin.site.register(Admin)
@admin.register(Admin)
class Admin(admin.ModelAdmin):
    list_display = [ 'user_id', 'user', 'organization']
admin.site.register(Organization)
admin.site.register(Users)