from django.shortcuts import render, render_to_response, redirect
from django.http import Http404
# from .forms import AddTaskForm, AddUserForm, ChangeTaskForm

#from django.views.decorators.csrf import csrf_protect
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from .models import ScrummyUser, ScrummyGoals, GoalStatus, Users
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import permission_required
# from django.contrib.auth.models import User
from django import template
from django.views import generic
from rest_framework import routers, serializers, viewsets
from .serializer import ScrummyUserSerializer, ScrummyGoalsSerializer, GoalStatusSerializer
from django.shortcuts import redirect
from myapp.forms import AdminSignUpForm, OrganizationForm, UserForm, ScrummyForm, AddTaskForm, AddStatusForm, ChangeTaskForm
from django.views.generic import CreateView
from django.contrib.auth import login, authenticate
from django.db import transaction
from django.contrib import messages
from django.shortcuts import get_object_or_404

def index(request):
    if request.user.is_authenticated:
        return redirect('myapp:home')
    return render(request, 'myapp/index.html')

def home(request):

    try:
        # users = User.objects.all().select_related('scrummyuser')
        users = Users.objects.all().select_related('scrummyuser')
        num_user = ScrummyUser.objects.all()
        task = GoalStatus.objects.all()
        con = {'user':num_user, 'task':task, 'users':users}
        return render(request, 'myapp/home.html', con)
    except ScrummyUser.DoesNotExist as e:
        raise Http404("Object does not exist")

def signup(request):
    if request.method == 'POST':
        adminForm = AdminSignUpForm(request.POST)
        # orgForm = OrganizationForm(request.POST)
        if adminForm.is_valid():
            adminForm.save()
            # orgForm.save()
            username = adminForm.cleaned_data.get('username')
            raw_password = adminForm.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, ('Your profile was successfully created!'))
            return redirect('myapp:home')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:

        adminForm = AdminSignUpForm()
        # orgForm = OrganizationForm()

    return render(request, 'registration/signup_form.html', {'form': adminForm})


def signup_profile(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():

            user = form.save()
            # user.is_active = False
            user.save()

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('myapp:home')
    else:
        form = UserForm()

    return render(request, 'registration/user_signup.html', {
            'form': form,

        })

# @transaction.atomic
# def signup_profile(request):
#     if request.method == 'POST':
#         user_form = UserForm(request.POST)
#         profile_form = ScrummyForm(request.POST)
#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             profile_form.save()
#             username = user_form.cleaned_data.get('username')
#             raw_password = user_form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=raw_password)
#             login(request, user)
#             messages.success(request, ('Your profile was successfully created!'))
#             return redirect('myapp:home')
#         else:
#             messages.error(request, ('Please correct the error below.'))
#     else:
#         user_form = UserForm()
#         profile_form = ScrummyForm()
#     return render(request, 'registration/user_signup.html', {
#         'user_form': user_form,
#         'profile_form': profile_form
#     })



def filter(request, task_id):
    var = GoalStatus.objects.filter(pk=task_id)
    out = " ".join([q.day_target for q in var])
    return HttpResponse("The Goal status for day target id %s is %s " % (task_id, out))

def move_goal(request, ta_id):
    mssg = ""

    if request.user.is_authenticated:
        # curr_user = request.user
        curr_user_group = request.user.scrummyuser.role
        admin = request.user.is_admin

        try:
            task = ScrummyGoals.objects.get(id=ta_id)
            task_status = task.target_name
        except ScrummyGoals.DoesNotExist:
            raise Http404("There is no task with id ")

        if curr_user_group:

            if request.method == "POST":
                form = ChangeTaskForm(request.POST or None, instance=task)

                if form.is_valid():
                    my_status = request.POST.get('target_name')
                    status_obj = GoalStatus.objects.get(id=my_status)

                        #Owner Permission
                    if admin:
                        task_status = status_obj
                        pass
                        # admin permission
                    elif str(curr_user_group) == 'AD':
                        if str(task_status) == 'Day' and status_obj.target == 'Verify':
                            task_status = status_obj
                        else:
                            messages.error(request, ('You do not have permission to move this task, '
                                                     'You can only move from Daily task to Verify'))
                            return redirect('myapp:home')
                            # return HttpResponse("You do not have permission to move this task, "
                            #                     "You can only move from Daily task to Verify")

                            # Quality analyst permission
                    elif str(curr_user_group) == 'QA':
                        if str(task_status) == 'Verify' and status_obj.target == 'Done':
                            task_status = status_obj
                        else:
                            messages.error(request, ('You do not have permission to move this task,'
                                                     ' You can only move from verify to Done'))
                            return redirect('myapp:home')
                            # return HttpResponse("You do not have permission to move this task,"
                            #                     " You can only move from verify to Done")

                            # Developer permission
                    elif str(curr_user_group) == 'DEV':
                        if str(task_status) == "Week" and status_obj.target == "Day" or str(task_status) == "Day" and status_obj.target =="Week":
                            task_status = status_obj
                        else:
                            messages.error(request, ('You do not have permission to move this task!'))
                            return redirect('myapp:home')
                            # return HttpResponse("You do not have permission to move this task,"
                            #                     " You can only move from Weekly target to Daily target")

                    else:
                        messages.error(request, ('You do not have permission to change the goal status!'))
                        return redirect('myapp:home')
                        # mssg += 'You do not have permission to change the goal status'
                        # return HttpResponse('No permission defined for your group')
                    task.save()

                    messages.success(request, ('Your status was successfully created!'))
                    return redirect('myapp:home')

            else:
                form = ChangeTaskForm()

            args = {'form': form}

            return render(request, 'myapp/move_task.html', args)
        else:
            return HttpResponse("User does not belong to any group")
    else:
        return HttpResponse("Access denied")
#
def add_task(request):
    try:
        if request.POST:
            form = AddTaskForm(request.POST)
            if form.is_valid():
                form.save()

                return redirect('myapp:home')

        else:
            form = AddTaskForm()

        args = {'form':form}

        return render(request, 'myapp/add_task.html', args)
    except ScrummyGoals.DoesNotExist:
        raise Http404("No records exists for this id")

def add_status(request):
    if request.POST:
        form = AddStatusForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, ('Your status was successfully created!'))
            return redirect('myapp:home')
    else:

        form = AddStatusForm()

        args = {'form':form}

    return render(request, 'myapp/add_status.html', args)

# def add_user(request):
#     if request.POST:
#        # user_form = UserForm(request.POST, instance=request.user)
#         my_form = AddUserForm(request.POST)
#         if  my_form.is_valid():
#             #user_form.save()
#             my_form.save()
#             return redirect('myapp:index')
#
#     else:
#         #user_form = UserForm()
#         my_form = AddUserForm()
#
#     args = {'my_form':my_form}
#
#     return render(request, 'myapp/add_user.html', args)

def user_add_task(request):
    week_status = GoalStatus.objects.get(target="Week")
    day_status = GoalStatus.objects.get(target="Day")
    verify_status = GoalStatus.objects.get(target="Verify")
    done_status = GoalStatus.objects.get(target="Done")
    # target = GoalStatus.objects.prefetch_related('scrummygoals')
    status = GoalStatus.objects.all()
    # target = ScrummyGoals.objects.get(target_name_id=week_status.id)


    if request.method == 'POST':
        if request.POST.get('task') and request.POST.get('goal'):
            task = ScrummyGoals()
            task.target_name_id = int(request.POST.get('goal'))
            task.user_name = request.user.scrummyuser
            task.task = request.POST.get('task')
            task.save()
            messages.success(request, ('Your task was successfully created!'))
            return redirect('myapp:home')

    con = {
        'week_status': week_status,
        'day_status': day_status,
        'verify_status': verify_status,
        'done_status': done_status,
        'status':status,
        # 'target':target
    }
    return render(request, 'myapp/user_add_task.html', con)

def user_delete(request, pk, template_name='myapp/delete_user.html'):
    # users = get_object_or_404(Users, pk=pk)
    scrummyusers = get_object_or_404(ScrummyUser, pk=pk)
    if request.method=='POST':
        # users.delete()
        scrummyusers.delete()
        messages.success(request, ('User was successfully deleted!'))
        return redirect('myapp:home')

    con = { 'scrummyusers':scrummyusers}
    return render(request, template_name, con)

class GoalView(generic.ListView):
    template_name = "myapp/goals.html"
    context_object_name = 'task_list'

    def get_queryset(self):
        return ScrummyGoals.objects.all()


class ScrummyUserViewSet(viewsets.ModelViewSet):
    queryset = ScrummyUser.objects.all()
    serializer_class = ScrummyUserSerializer


class ScrummyGoalsViewSet(viewsets.ModelViewSet):
    queryset = ScrummyGoals.objects.all()
    serializer_class = ScrummyGoalsSerializer


class GoalStatusViewSet(viewsets.ModelViewSet):
    queryset = GoalStatus.objects.all()
    serializer_class = GoalStatusSerializer





