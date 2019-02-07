from django.urls import path

from . import views
app_name = 'myapp'
urlpatterns = [
    path('', views.index, name='index'),
    path('filter/<int:task_id>/', views.filter, name='filter'),
    path('move/<int:ta_id>/',views.move_goal, name='move_goal'),
    path('task/',views.add_task, name='add_task'),
    path('adduser/', views.add_user, name='add_user'),
    path('goals/', views.GoalView.as_view(), name='goal'),
    path('home/', views.home, name='home'),
    #path('scrummy/', views.ScrummyUserViewSet.as_view('list'), name='scrummy'),


]