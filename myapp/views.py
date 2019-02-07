from django.shortcuts import render, render_to_response, redirect
from django.http import Http404
from .forms import AddTaskForm, AddUserForm, ChangeTaskForm

#from django.views.decorators.csrf import csrf_protect
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from .models import ScrummyUser, ScrummyGoals, GoalStatus
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django import template
from django.views import generic
from rest_framework import routers, serializers, viewsets
from .serializer import ScrummyUserSerializer, ScrummyGoalsSerializer, GoalStatusSerializer

def index(request):

    try:
        users = User.objects.all().select_related('scrummyuser')
        num_user = ScrummyUser.objects.all()
        task = GoalStatus.objects.all()
        con = {'user':num_user, 'task':task, 'users':users}
        return render(request, 'myapp/index.html', con)
    except ScrummyUser.DoesNotExist as e:
        raise Http404("Object does not exist")


def filter(request, task_id):
    var = GoalStatus.objects.filter(pk=task_id)
    out = " ".join([q.day_target for q in var])
    return HttpResponse("The Goal status for day target id %s is %s " % (task_id, out))

def move_goal(request, ta_id):
    mssg = ""

    if request.user.is_authenticated:
        curr_user = request.user
        curr_user_group = curr_user.groups.all()

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
                    if str(curr_user_group[0]) == 'OWNER':
                        task_status = status_obj
                        pass
                        # admin permission
                    elif str(curr_user_group[0]) == 'ADMIN':
                        if str(task_status) == 'Day' and status_obj.target == 'Verify':
                            task_status = status_obj
                        else:
                            return HttpResponse("You do not have permission to move this task, "
                                                "You can only move from Daily task to Verify")

                            # Quality analyst permission
                    elif str(curr_user_group[0]) == 'QA':
                        if str(task_status) == 'Verify' and status_obj.target == 'Done':
                            task_status = status_obj
                        else:
                            return HttpResponse("You do not have permission to move this task,"
                                                " You can only move from verify to Done")

                            # Developer permission
                    elif str(curr_user_group[0]) == 'DEVELOPER':
                        if str(task_status) == "Week" and status_obj.target == "Day" or str(task_status) == "Day" and status_obj.target =="Week":
                            task_status = status_obj
                        else:
                            return HttpResponse("You do not have permission to move this task,"
                                                " You can only move from Weekly target to Daily target")

                    else:
                        mssg += 'You do not have permission to change the goal status'
                        return HttpResponse('No permission defined for your group')
                    task.save()

                    return redirect('myapp:index')

            else:
                form = ChangeTaskForm()

            args = {'form': form}

            return render(request, 'myapp/move_task.html', args)
        else:
            return HttpResponse("User does not belong to any group")
    else:
        return HttpResponse("Access denied")

def add_task(request):
    try:
        if request.POST:
            form = AddTaskForm(request.POST)
            if form.is_valid():
                form.save()

                return redirect('myapp:index')

        else:
            form = AddTaskForm()

        args = {'form':form}

        return render(request, 'myapp/add_task.html', args)
    except ScrummyGoals.DoesNotExist:
        raise Http404("No records exists for this id")



def add_user(request):
    if request.POST:
       # user_form = UserForm(request.POST, instance=request.user)
        my_form = AddUserForm(request.POST)
        if  my_form.is_valid():
            #user_form.save()
            my_form.save()
            return redirect('myapp:index')

    else:
        #user_form = UserForm()
        my_form = AddUserForm()

    args = {'my_form':my_form}

    return render(request, 'myapp/add_user.html', args)

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



def home(request):
    return render_to_response('myapp/home.html')

