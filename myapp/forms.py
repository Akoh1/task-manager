from django.forms import ModelForm
from django import forms
from .models import ScrummyUser, ScrummyGoals, GoalStatus, Organization, Users, Admin
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.forms import UserCreationForm
# from myapp.models import User, ScrummyUser, Admin, Organization
from django.db import transaction
from .choice import role
from django.contrib.auth.models import User


class OrganizationForm(forms.ModelForm):

    # organization = forms.CharField(max_length=255)

    class Meta:
        model = Organization
        fields = ['organization']



class AdminSignUpForm(UserCreationForm):
    organization = forms.CharField(required=True, max_length=255, widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta(UserCreationForm.Meta):
        model = Users
        fields = ['username','email','organization']

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_admin = True
        user.save()
        organization = self.cleaned_data.get('organization')
        admin = Admin()
        admin.organization = organization
        admin.save()
        # if commit:
        #     user.save()
        return user



class UserForm(UserCreationForm):
    role = forms.ChoiceField(choices=role)
    org = forms.ModelChoiceField(
        queryset=Admin.objects.all(),
    )
    class Meta:
        model = Users
        fields = ('first_name', 'last_name', 'email','username','role', 'org')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_user = True
        user.save()
        role = self.cleaned_data.get('role')
        org = self.cleaned_data.get('org')
        profile = ScrummyUser()
        profile.user = user
        profile.role =role
        profile.org = org
        profile.save()

        return user


class ScrummyForm(forms.ModelForm):
    class Meta:
        model = ScrummyUser
        fields = ( 'role', 'org')

class ChangeTaskForm(forms.ModelForm):
    class Meta:
        model = ScrummyGoals
        fields = ['target_name']
#
#
#
# class AddUserForm(forms.ModelForm):
#
#     password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
#     password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
#     class Meta:
#
#         model = ScrummyUser
#         widgets = {'password1' : forms.PasswordInput(render_value=True), 'password2' : forms.PasswordInput(render_value=True)}
#
#         fields = ['first_name','last_name','username','password1','password2']
#
#     def clean_password2(self):
#         password1 = self.cleaned_data.get("password1")
#         password2 = self.cleaned_data.get('password2')
#
#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError("Password Dont match")
#         return password2
#
#     def save(self, commit=True):
#         user = super(AddUserForm, self).save(commit=False)
#         user.set_password(self.cleaned_data["password1"])
#         user.is_active = False
#         if commit:
#             user.save()
#         return user

class AddTaskForm(forms.ModelForm):


    class Meta:
        model = ScrummyGoals
        fields = ['task','target_name','user_name']


class AddStatusForm(forms.ModelForm):
    class Meta:
        model = GoalStatus
        fields = ['target']
